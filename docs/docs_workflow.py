#!/usr/bin/env python
"""
Automated Documentation Workflow Script

This script automates the entire documentation workflow:
1. Validates existing documentation
2. Generates documentation from docstrings
3. Converts Markdown to RST if needed
4. Builds documentation into different formats
5. Reports any issues
"""

import os
import sys
import argparse
import subprocess
import re
from datetime import datetime

def run_command(command):
    """Execute a shell command and return output."""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        universal_newlines=True
    )
    stdout, stderr = process.communicate()
    return process.returncode, stdout, stderr

def validate_docs():
    """Validate all documentation files."""
    print("Validating documentation...")
    return run_command("python manage.py manage_docs validate")

def generate_app_docs(app_names):
    """Generate documentation from docstrings for given apps."""
    print(f"Generating documentation for apps: {', '.join(app_names)}")
    results = []
    for app in app_names:
        print(f"  Processing {app}...")
        results.append(run_command(f"python manage.py manage_docs generate --app {app} --validate"))
    return results

def convert_markdown_to_rst():
    """Convert Markdown files to RST format."""
    print("Converting Markdown files to RST...")
    
    try:
        import pypandoc
    except ImportError:
        print("  Error: pypandoc not installed. Run: pip install pypandoc")
        return 1, "", "pypandoc not installed"
    
    # Find all Markdown files in project
    md_files = []
    for root, dirs, files in os.walk('.'):
        if '.venv' in root or 'node_modules' in root:
            continue
        for file in files:
            if file.endswith('.md') and not file == 'README.md':
                md_files.append(os.path.join(root, file))
    
    if not md_files:
        print("  No Markdown files found to convert")
        return 0, "", ""
    
    for md_file in md_files:
        rst_file = f"docs/{os.path.splitext(os.path.basename(md_file))[0]}.rst"
        print(f"  Converting {md_file} to {rst_file}")
        
        # Read markdown content
        with open(md_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert to RST
        rst_content = pypandoc.convert_text(md_content, 'rst', format='md')
        
        # Add title and last updated
        title = os.path.splitext(os.path.basename(md_file))[0].replace('_', ' ').title()
        rst_content = f"{title}\n{'=' * len(title)}\n\nLast updated: {datetime.now().strftime('%Y-%m-%d')}\n\n{rst_content}"
        
        # Write RST file
        with open(rst_file, 'w', encoding='utf-8') as f:
            f.write(rst_content)
        
        # Add to index
        code, stdout, stderr = run_command(f"python manage.py manage_docs update --file {os.path.splitext(os.path.basename(md_file))[0]} --content ''")
        if code != 0:
            print(f"  Warning: Could not update index.rst for {rst_file}")
    
    return 0, f"Converted {len(md_files)} files", ""

def extract_code_comments():
    """Extract code comments from source files and generate documentation."""
    print("Extracting comments from source code...")
    
    # Extensions and their comment markers
    comment_markers = {
        '.py': '#',
        '.js': '//',
        '.css': '/*',
        '.html': '<!--',
    }
    
    doc_sections = {}
    
    # Find all source files
    for root, dirs, files in os.walk('quiz_app'):
        if '.venv' in root or 'node_modules' in root or '__pycache__' in root:
            continue
        
        for file in files:
            ext = os.path.splitext(file)[1]
            if ext not in comment_markers:
                continue
                
            full_path = os.path.join(root, file)
            marker = comment_markers[ext]
            
            # Read the file
            with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract documentation comments
            if ext == '.py':
                # Python: Look for triple-quoted docstrings
                doc_pattern = r'"""(.*?)"""'
                matches = re.findall(doc_pattern, content, re.DOTALL)
                if matches:
                    rel_path = os.path.relpath(full_path, '.')
                    doc_sections[rel_path] = matches
            else:
                # Other languages: Look for block comments
                if marker == '//':
                    doc_pattern = r'//\s*@doc\s+(.*?)$'
                    matches = re.findall(doc_pattern, content, re.MULTILINE)
                    if matches:
                        rel_path = os.path.relpath(full_path, '.')
                        doc_sections[rel_path] = matches
                elif marker == '/*':
                    doc_pattern = r'/\*\*\s*(.*?)\*/'
                    matches = re.findall(doc_pattern, content, re.DOTALL)
                    if matches:
                        rel_path = os.path.relpath(full_path, '.')
                        doc_sections[rel_path] = matches
                elif marker == '<!--':
                    doc_pattern = r'<!--\s*@doc\s+(.*?)-->'
                    matches = re.findall(doc_pattern, content, re.DOTALL)
                    if matches:
                        rel_path = os.path.relpath(full_path, '.')
                        doc_sections[rel_path] = matches
    
    if not doc_sections:
        print("  No additional documentation comments found")
        return 0, "", ""
    
    # Create a documentation file from extracted comments
    rst_file = "docs/code_comments.rst"
    with open(rst_file, 'w', encoding='utf-8') as f:
        f.write(f"""Code Comments Documentation
========================

Last updated: {datetime.now().strftime('%Y-%m-%d')}

This document contains documentation extracted from comments in the source code.

""")
        
        for file_path, doc_blocks in doc_sections.items():
            f.write(f"\n{file_path}\n{'-' * len(file_path)}\n\n")
            for block in doc_blocks:
                f.write(f"{block.strip()}\n\n")
    
    # Add to index
    code, stdout, stderr = run_command("python manage.py manage_docs update --file code_comments --content ''")
    if code != 0:
        print("  Warning: Could not update index.rst for code_comments.rst")
    
    return 0, f"Extracted documentation from {len(doc_sections)} files", ""

def build_docs():
    """Build documentation in various formats."""
    print("Building documentation...")
    
    # Build HTML
    print("  Building HTML documentation...")
    code_html, stdout_html, stderr_html = run_command("sphinx-build -b html docs docs/_build/html")
    
    # Build LaTeX
    print("  Building LaTeX documentation...")
    code_latex, stdout_latex, stderr_latex = run_command("sphinx-build -b latex docs docs/_build/latex")
    
    # Build PDF if LaTeX build succeeded and pdflatex is available
    if code_latex == 0:
        print("  Building PDF documentation...")
        pdf_cmd = run_command("pdflatex --version")
        if pdf_cmd[0] == 0:
            # Change to LaTeX directory, run pdflatex, and return
            os.chdir("docs/_build/latex")
            code_pdf, stdout_pdf, stderr_pdf = run_command("pdflatex *.tex")
            os.chdir("../../..")
        else:
            print("  Warning: pdflatex not available for PDF generation")
            code_pdf, stdout_pdf, stderr_pdf = 1, "", "pdflatex not available"
    else:
        code_pdf, stdout_pdf, stderr_pdf = 1, "", "LaTeX build failed"
    
    # Build Word Document
    print("  Building Word documentation...")
    code_docx, stdout_docx, stderr_docx = run_command("sphinx-build -b docx docs docs/_build/docx")
    
    results = [
        ("HTML", code_html, stderr_html),
        ("LaTeX", code_latex, stderr_latex),
        ("PDF", code_pdf, stderr_pdf),
        ("Word", code_docx, stderr_docx)
    ]
    
    return results

def main():
    """Main function to run the documentation workflow."""
    parser = argparse.ArgumentParser(description="Automated Documentation Workflow")
    parser.add_argument('--apps', nargs='+', default=['quiz_app'], help='Django apps to generate docs for')
    parser.add_argument('--skip-validation', action='store_true', help='Skip validation step')
    parser.add_argument('--skip-generation', action='store_true', help='Skip docstring generation step')
    parser.add_argument('--skip-md-conversion', action='store_true', help='Skip Markdown conversion step')
    parser.add_argument('--skip-comments', action='store_true', help='Skip extracting code comments')
    parser.add_argument('--skip-build', action='store_true', help='Skip documentation building step')
    parser.add_argument('--output-format', choices=['html', 'latex', 'pdf', 'word', 'all'], default='all',
                       help='Output format(s) to generate')
    
    args = parser.parse_args()
    
    print(f"Starting documentation workflow at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Validation
    if not args.skip_validation:
        code, stdout, stderr = validate_docs()
        if code != 0:
            print(f"Warning: Documentation validation had issues:\n{stderr}")
        else:
            print("Documentation validation completed successfully")
    
    # Generate docs from docstrings
    if not args.skip_generation:
        results = generate_app_docs(args.apps)
        for i, (app, (code, stdout, stderr)) in enumerate(zip(args.apps, results)):
            if code != 0:
                print(f"Warning: Documentation generation for {app} had issues:\n{stderr}")
            else:
                print(f"Documentation generation for {app} completed successfully")
    
    # Convert Markdown to RST
    if not args.skip_md_conversion:
        code, stdout, stderr = convert_markdown_to_rst()
        if code != 0:
            print(f"Warning: Markdown conversion had issues:\n{stderr}")
        else:
            print(f"Markdown conversion completed: {stdout}")
    
    # Extract code comments
    if not args.skip_comments:
        code, stdout, stderr = extract_code_comments()
        if code != 0:
            print(f"Warning: Comment extraction had issues:\n{stderr}")
        else:
            print(f"Comment extraction completed: {stdout}")
    
    # Build documentation
    if not args.skip_build:
        results = build_docs()
        for format_name, code, stderr in results:
            if args.output_format != 'all' and format_name.lower() != args.output_format:
                continue
                
            if code != 0:
                print(f"Warning: {format_name} build had issues:\n{stderr}")
            else:
                print(f"{format_name} build completed successfully")
    
    print(f"Documentation workflow completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("\nDocumentation available at:")
    print("  HTML: docs/_build/html/index.html")
    print("  Word: docs/_build/docx/QuizGame.docx")
    print("  LaTeX: docs/_build/latex/*.tex")
    print("  PDF: docs/_build/latex/*.pdf (if PDF generation succeeded(probably not))")

if __name__ == "__main__":
    main() 