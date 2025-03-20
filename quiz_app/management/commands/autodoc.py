#!/usr/bin/env python
"""
Complete Documentation Automation Workflow

This script automates the entire documentation workflow:
1. Generating documentation from multiple sources
2. Validating documentation
3. Building documentation in various formats
4. Deploying documentation (optional)
"""

import os
import re
import sys
import json
import argparse
import subprocess
import importlib
import inspect
import glob
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

import django
from django.core.management.base import BaseCommand
from django.apps import apps

# Add support for markdown
try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False

# Import doc utilities
from .doc_templates import TEMPLATES
from .doc_validator import DocValidator
from .doc_generator import DocGenerator


class MarkdownConverter:
    """Converts Markdown to reStructuredText."""
    
    @staticmethod
    def md_to_rst(md_content: str) -> str:
        """Convert Markdown content to RST."""
        if not MARKDOWN_AVAILABLE:
            raise ImportError("markdown package is required for Markdown conversion. Install with pip install markdown")
        
        # First convert to HTML
        html_content = markdown.markdown(md_content, extensions=['tables', 'fenced_code', 'codehilite'])
        
        # Then, convert HTML to RST
        # This is a simplified version; for complex docs you might want a more robust solution
        # like pandoc or a dedicated HTML to RST converter
        
        # Process headers
        html_content = re.sub(r'<h1>(.*?)</h1>', r'\n\1\n' + '=' * 80 + '\n', html_content)
        html_content = re.sub(r'<h2>(.*?)</h2>', r'\n\1\n' + '-' * 80 + '\n', html_content)
        html_content = re.sub(r'<h3>(.*?)</h3>', r'\n\1\n' + '~' * 80 + '\n', html_content)
        
        # Process lists
        html_content = re.sub(r'<ul>(.*?)</ul>', r'\n\\1', html_content, flags=re.DOTALL)
        html_content = re.sub(r'<li>(.*?)</li>', r'\n* \\1', html_content)
        
        # Process code blocks
        html_content = re.sub(r'<pre><code>(.*?)</code></pre>', r'\n::\n\n    \\1\n', html_content, flags=re.DOTALL)
        
        # Process inline code
        html_content = re.sub(r'<code>(.*?)</code>', r'``\\1``', html_content)
        
        # Process links
        html_content = re.sub(r'<a href="(.*?)">(.*?)</a>', r'`\\2 <\\1>`_', html_content)
        
        # Process paragraphs
        html_content = re.sub(r'<p>(.*?)</p>', r'\n\\1\n', html_content)
        
        # Remove remaining HTML tags
        html_content = re.sub(r'<[^>]*>', '', html_content)
        
        return html_content


class CommentExtractor:
    """Extracts documentation from HTML, JavaScript, CSS, and Python comments."""
    
    @staticmethod
    def extract_from_html(file_path: str) -> str:
        """Extract documentation from HTML comments."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract HTML comments
        comments = re.findall(r'<!--\s*@doc\s*(.*?)\s*-->', content, re.DOTALL)
        
        if not comments:
            return ""
        
        rst_content = f"""HTML Documentation
==================

Last updated: {datetime.now().strftime('%Y-%m-%d')}

"""
        
        for comment in comments:
            # Process any special annotations
            if comment.startswith('title:'):
                title_match = re.match(r'title:(.*?)(\n|$)', comment)
                if title_match:
                    title = title_match.group(1).strip()
                    rst_content += f"\n{title}\n{'-' * len(title)}\n\n"
                    comment = comment[title_match.end():].strip()
            
            rst_content += f"{comment.strip()}\n\n"
        
        return rst_content
    
    @staticmethod
    def extract_from_js(file_path: str) -> str:
        """Extract documentation from JavaScript comments."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract JS doc comments
        comments = re.findall(r'/\*\*\s*@doc\s*(.*?)\s*\*/', content, re.DOTALL)
        
        if not comments:
            return ""
        
        rst_content = f"""JavaScript Documentation
=========================

Last updated: {datetime.now().strftime('%Y-%m-%d')}

"""
        
        for comment in comments:
            # Process any special annotations
            if comment.startswith('title:'):
                title_match = re.match(r'title:(.*?)(\n|$)', comment)
                if title_match:
                    title = title_match.group(1).strip()
                    rst_content += f"\n{title}\n{'-' * len(title)}\n\n"
                    comment = comment[title_match.end():].strip()
            
            # Replace JSDoc annotations with RST equivalents
            comment = re.sub(r'@param\s+\{([^}]+)\}\s+(\w+)', r':param \\2: ', comment)
            comment = re.sub(r'@returns?\s+\{([^}]+)\}', r':return: ', comment)
            
            rst_content += f"{comment.strip()}\n\n"
        
        return rst_content
    
    @staticmethod
    def extract_from_css(file_path: str) -> str:
        """Extract documentation from CSS comments."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract CSS comments
        comments = re.findall(r'/\*\s*@doc\s*(.*?)\s*\*/', content, re.DOTALL)
        
        if not comments:
            return ""
        
        rst_content = f"""CSS Documentation
================

Last updated: {datetime.now().strftime('%Y-%m-%d')}

"""
        
        for comment in comments:
            # Process any special annotations
            if comment.startswith('title:'):
                title_match = re.match(r'title:(.*?)(\n|$)', comment)
                if title_match:
                    title = title_match.group(1).strip()
                    rst_content += f"\n{title}\n{'-' * len(title)}\n\n"
                    comment = comment[title_match.end():].strip()
            
            rst_content += f"{comment.strip()}\n\n"
        
        return rst_content
    
    @staticmethod
    def extract_from_python(file_path: str) -> str:
        """Extract documentation from Python comments (beyond docstrings)."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract Python comments that are specifically marked for docs
        comments = re.findall(r'#\s*@doc\s*(.*?)(?=\n#\s*@doc|\n\w|$)', content, re.DOTALL)
        
        if not comments:
            return ""
        
        rst_content = f"""Python Comment Documentation
===========================

Last updated: {datetime.now().strftime('%Y-%m-%d')}

"""
        
        for comment in comments:
            # Process any special annotations
            if comment.startswith('title:'):
                title_match = re.match(r'title:(.*?)(\n|$)', comment)
                if title_match:
                    title = title_match.group(1).strip()
                    rst_content += f"\n{title}\n{'-' * len(title)}\n\n"
                    comment = comment[title_match.end():].strip()
            
            # Remove leading # and spaces from each line
            lines = [line.strip()[1:].lstrip() if line.strip().startswith('#') else line for line in comment.split('\n')]
            comment = '\n'.join(lines)
            
            rst_content += f"{comment.strip()}\n\n"
        
        return rst_content
    
    @staticmethod
    def extract_from_markdown(file_path: str) -> str:
        """Extract documentation from Markdown files."""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        converter = MarkdownConverter()
        return converter.md_to_rst(content)


class DocumentationWorkflow:
    """Complete documentation workflow automation."""
    
    def __init__(self, project_root: str = None):
        """Initialize with project root."""
        if project_root is None:
            self.project_root = os.getcwd()
        else:
            self.project_root = project_root
        
        self.docs_dir = os.path.join(self.project_root, 'docs')
        self.source_dir = os.path.join(self.docs_dir, 'source')
        self.build_dir = os.path.join(self.docs_dir, '_build')
        
        self.validator = DocValidator()
        self.doc_generator = DocGenerator()
        self.comment_extractor = CommentExtractor()
        
        self.ensure_dirs()
    
    def ensure_dirs(self):
        """Ensure all necessary directories exist."""
        os.makedirs(self.docs_dir, exist_ok=True)
        os.makedirs(self.source_dir, exist_ok=True)
        os.makedirs(self.build_dir, exist_ok=True)
    
    def find_files(self, pattern: str) -> List[str]:
        """Find files matching a pattern."""
        return glob.glob(os.path.join(self.project_root, pattern), recursive=True)
    
    def generate_from_docstrings(self, app_names: List[str]) -> Dict[str, str]:
        """Generate documentation from Python docstrings."""
        docs = {}
        for app_name in app_names:
            app_docs = self.doc_generator.generate_all_docs(app_name)
            for key, content in app_docs.items():
                docs[f"{app_name}_{key}"] = content
        return docs
    
    def generate_from_comments(self) -> Dict[str, str]:
        """Generate documentation from various file comments."""
        docs = {}
        
        # HTML files
        html_files = self.find_files('**/templates/**/*.html')
        html_content = ""
        for file in html_files:
            content = self.comment_extractor.extract_from_html(file)
            if content:
                rel_path = os.path.relpath(file, self.project_root)
                html_content += f"\n\nFrom {rel_path}:\n{'-' * (len(rel_path) + 6)}\n\n{content}"
        
        if html_content:
            docs['templates'] = f"""HTML Templates
==============

Last updated: {datetime.now().strftime('%Y-%m-%d')}

This document contains documentation extracted from HTML template comments.

{html_content}
"""
        
        # JavaScript files
        js_files = self.find_files('**/static/**/*.js')
        js_content = ""
        for file in js_files:
            content = self.comment_extractor.extract_from_js(file)
            if content:
                rel_path = os.path.relpath(file, self.project_root)
                js_content += f"\n\nFrom {rel_path}:\n{'-' * (len(rel_path) + 6)}\n\n{content}"
        
        if js_content:
            docs['javascript'] = f"""JavaScript
==========

Last updated: {datetime.now().strftime('%Y-%m-%d')}

This document contains documentation extracted from JavaScript files.

{js_content}
"""
        
        # CSS files
        css_files = self.find_files('**/static/**/*.css')
        css_content = ""
        for file in css_files:
            content = self.comment_extractor.extract_from_css(file)
            if content:
                rel_path = os.path.relpath(file, self.project_root)
                css_content += f"\n\nFrom {rel_path}:\n{'-' * (len(rel_path) + 6)}\n\n{content}"
        
        if css_content:
            docs['css'] = f"""CSS Styles
=========

Last updated: {datetime.now().strftime('%Y-%m-%d')}

This document contains documentation extracted from CSS files.

{css_content}
"""
        
        # Python files with @doc comments (beyond docstrings)
        py_files = self.find_files('**/*.py')
        py_content = ""
        for file in py_files:
            content = self.comment_extractor.extract_from_python(file)
            if content:
                rel_path = os.path.relpath(file, self.project_root)
                py_content += f"\n\nFrom {rel_path}:\n{'-' * (len(rel_path) + 6)}\n\n{content}"
        
        if py_content:
            docs['python_comments'] = f"""Python Comments
==============

Last updated: {datetime.now().strftime('%Y-%m-%d')}

This document contains documentation extracted from Python comments.

{py_content}
"""
        
        return docs
    
    def generate_from_markdown(self) -> Dict[str, str]:
        """Generate documentation from Markdown files."""
        docs = {}
        
        # Find markdown files
        md_files = self.find_files('**/*.md')
        for file in md_files:
            # Skip files in the docs directory and venv
            if 'docs/' in file or '.venv/' in file or 'node_modules/' in file:
                continue
                
            try:
                content = self.comment_extractor.extract_from_markdown(file)
                if content:
                    # Use the filename (without extension) as the key
                    key = os.path.splitext(os.path.basename(file))[0].lower()
                    # Avoid overwriting existing docs
                    if key in docs:
                        key = f"{key}_{len(docs)}"
                    docs[key] = content
            except Exception as e:
                print(f"Error processing markdown file {file}: {e}")
        
        return docs
    
    def write_docs(self, docs: Dict[str, str]) -> List[str]:
        """Write documentation to RST files."""
        written_files = []
        
        for name, content in docs.items():
            # Skip empty content
            if not content.strip():
                continue
                
            file_path = os.path.join(self.source_dir, f"{name}.rst")
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            written_files.append(file_path)
            
            print(f"Created: {file_path}")
        
        return written_files
    
    def update_index(self, rst_files: List[str]):
        """Update index.rst with new files."""
        index_path = os.path.join(self.source_dir, 'index.rst')
        
        # Create default index if it doesn't exist
        if not os.path.exists(index_path):
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(f"""Welcome to Django Quiz Documentation
================================

Last updated: {datetime.now().strftime('%Y-%m-%d')}

.. toctree::
   :maxdepth: 2
   :caption: Contents:

""")
        
        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find toctree section
        toctree_match = re.search(r'(\.\. toctree::\n\s+:maxdepth: \d+\n\s+:caption: [^\n]+\n\n)((?:\s+[^\n]+\n)*)', content)
        
        if toctree_match:
            toctree_start = toctree_match.group(1)
            existing_entries = toctree_match.group(2)
            
            # Build updated entries
            entries = []
            for line in existing_entries.splitlines():
                if line.strip():
                    entries.append(line.strip())
            
            # Add new files that aren't already in the toctree
            for file_path in rst_files:
                name = os.path.splitext(os.path.basename(file_path))[0]
                if name not in existing_entries:
                    entries.append(name)
            
            # Create updated toctree
            new_toctree = toctree_start + '\n   '.join([''] + sorted(entries)) + '\n\n'
            
            # Replace toctree in content
            new_content = content.replace(toctree_match.group(0), new_toctree)
            
            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
            print(f"Updated toctree in {index_path}")
    
    def validate_docs(self):
        """Validate all documentation files."""
        issues_found = False
        
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                if file.endswith('.rst'):
                    file_path = os.path.join(root, file)
                    
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    issues = self.validator.validate_rst_file(content)
                    
                    if issues:
                        issues_found = True
                        print(f"\nIssues found in {file_path}:")
                        for issue in issues:
                            print(f"Line {issue['line']}: {issue['message']} ({issue['type']})")
                    else:
                        print(f"No issues found in {file_path}")
        
        return not issues_found
    
    def build_docs(self, formats: List[str] = None):
        """Build documentation in various formats."""
        if formats is None:
            formats = ['html']
        
        for format in formats:
            try:
                subprocess.run([
                    'sphinx-build',
                    '-b', format,
                    self.source_dir,
                    os.path.join(self.build_dir, format)
                ], check=True)
                print(f"Successfully built {format} documentation")
            except subprocess.CalledProcessError as e:
                print(f"Error building {format} documentation: {e}")
    
    def run_workflow(self, app_names: List[str], formats: List[str] = None):
        """Run the complete documentation workflow."""
        print("Starting documentation workflow...")
        
        # Generate documentation from various sources
        docs = {}
        
        # From docstrings
        print("\nGenerating documentation from docstrings...")
        docstring_docs = self.generate_from_docstrings(app_names)
        docs.update(docstring_docs)
        
        # From comments
        print("\nGenerating documentation from comments...")
        comment_docs = self.generate_from_comments()
        docs.update(comment_docs)
        
        # From markdown
        print("\nGenerating documentation from Markdown...")
        markdown_docs = self.generate_from_markdown()
        docs.update(markdown_docs)
        
        # Write docs to files
        print("\nWriting documentation files...")
        rst_files = self.write_docs(docs)
        
        # Update index
        print("\nUpdating index...")
        self.update_index(rst_files)
        
        # Validate docs
        print("\nValidating documentation...")
        validation_ok = self.validate_docs()
        
        if validation_ok:
            print("\nValidation successful. Building documentation...")
            # Build docs
            self.build_docs(formats)
            print("\nDocumentation workflow completed successfully!")
        else:
            print("\nValidation found issues. Please fix them before building.")
            
        return validation_ok


class Command(BaseCommand):
    help = 'Automates the entire documentation workflow'

    def add_arguments(self, parser):
        parser.add_argument('--apps', nargs='+', help='App names to document')
        parser.add_argument(
            '--formats', 
            nargs='+', 
            default=['html', 'docx'], 
            help='Output formats (html, docx, pdf, etc.)'
        )
        parser.add_argument(
            '--skip-validation', 
            action='store_true', 
            help='Skip validation step'
        )
        parser.add_argument(
            '--comments-only', 
            action='store_true', 
            help='Only extract from comments, not docstrings'
        )
        parser.add_argument(
            '--markdown-only', 
            action='store_true', 
            help='Only convert markdown files'
        )

    def handle(self, *args, **options):
        apps = options.get('apps') or []
        formats = options.get('formats') or ['html', 'docx']
        
        # If no apps specified, use all installed apps
        if not apps:
            apps = [app.label for app in apps.get_app_configs() 
                    if not app.label.startswith('django.')]
            
        workflow = DocumentationWorkflow()
        
        if options.get('comments_only'):
            docs = workflow.generate_from_comments()
            rst_files = workflow.write_docs(docs)
            workflow.update_index(rst_files)
            if not options.get('skip_validation'):
                workflow.validate_docs()
            workflow.build_docs(formats)
        elif options.get('markdown_only'):
            docs = workflow.generate_from_markdown()
            rst_files = workflow.write_docs(docs)
            workflow.update_index(rst_files)
            if not options.get('skip_validation'):
                workflow.validate_docs()
            workflow.build_docs(formats)
        else:
            workflow.run_workflow(apps, formats)
        
        self.stdout.write(self.style.SUCCESS(
            f'Documentation generated and built in {workflow.build_dir}'))


if __name__ == '__main__':
    # This allows the script to be run directly for testing
    parser = argparse.ArgumentParser(description='Automate documentation workflow')
    parser.add_argument('--apps', nargs='+', help='App names to document')
    parser.add_argument(
        '--formats', 
        nargs='+', 
        default=['html'], 
        help='Output formats (html, docx, pdf, etc.)'
    )
    
    args = parser.parse_args()
    
    # Setup Django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
    django.setup()
    
    workflow = DocumentationWorkflow()
    workflow.run_workflow(args.apps or [], args.formats or ['html']) 