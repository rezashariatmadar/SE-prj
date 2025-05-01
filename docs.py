#!/usr/bin/env python
"""
Documentation workflow automation script

This script provides a simple CLI to run the documentation automation workflow.
It automates the generation of documentation in various formats, manages documentation
dependencies, and provides tools for opening and viewing the generated documentation.
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def setup_environment():
    """
    Set up the Python environment.
    
    This function attempts to activate the virtual environment if it exists
    and is not already activated. This ensures that the script runs with
    the correct Python interpreter and has access to all required packages.
    """
    # Get the absolute path to the Django project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Activate virtual environment if needed
    if not os.environ.get('VIRTUAL_ENV'):
        venv_dir = os.path.join(script_dir, '.venv')
        if os.path.exists(venv_dir):
            if sys.platform == 'win32':
                activate_script = os.path.join(venv_dir, 'Scripts', 'activate_this.py')
            else:
                activate_script = os.path.join(venv_dir, 'bin', 'activate_this.py')
            
            if os.path.exists(activate_script):
                with open(activate_script) as f:
                    exec(f.read(), {'__file__': activate_script})
                print(f"Activated virtual environment: {venv_dir}")
            else:
                print("Warning: Virtual environment found but activate_this.py not found")
        else:
            print("Warning: No virtual environment found at .venv")


def validate_project():
    """
    Validate that we're in a Django project root.
    
    This ensures the script is being run from the correct directory by
    checking for the presence of manage.py, which is a standard file
    in Django projects.
    """
    if not os.path.exists('manage.py'):
        print("Error: manage.py not found. Please run this script from your Django project root.")
        sys.exit(1)


def run_autodoc(args):
    """
    Run the autodoc command with given arguments.
    
    This function executes the Django management command 'autodoc'
    with the provided arguments to generate documentation from the codebase.
    
    Args:
        args: An object containing command line arguments for the autodoc command.
    """
    cmd = ['python', 'manage.py', 'autodoc']
    
    if args.apps:
        cmd.extend(['--apps'] + args.apps)
    
    if args.formats:
        cmd.extend(['--formats'] + args.formats)
    
    if args.skip_validation:
        cmd.append('--skip-validation')
    
    if args.comments_only:
        cmd.append('--comments-only')
    
    if args.markdown_only:
        cmd.append('--markdown-only')
    
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running autodoc: {e}")
        sys.exit(1)


def open_docs(format_type):
    """
    Open the generated documentation.
    
    This function locates and opens the generated documentation in the
    specified format using the appropriate system application.
    
    Args:
        format_type: The format of documentation to open ('html', 'docx', or 'pdf').
    """
    docs_dir = os.path.join(os.getcwd(), 'docs', '_build')
    
    if format_type == 'html':
        # Open HTML documentation in the default web browser
        index_path = os.path.join(docs_dir, 'html', 'index.html')
        if os.path.exists(index_path):
            if sys.platform == 'win32':
                os.startfile(index_path)
            else:
                import webbrowser
                webbrowser.open(f'file://{index_path}')
        else:
            print(f"Error: HTML documentation not found at {index_path}")
    
    elif format_type == 'docx':
        # Open Word documentation in the default application
        docx_dir = os.path.join(docs_dir, 'docx')
        if os.path.exists(docx_dir):
            docx_files = [f for f in os.listdir(docx_dir) if f.endswith('.docx')]
            if docx_files:
                docx_path = os.path.join(docx_dir, docx_files[0])
                if sys.platform == 'win32':
                    os.startfile(docx_path)
                else:
                    subprocess.run(['xdg-open', docx_path], check=False)
            else:
                print(f"Error: No .docx files found in {docx_dir}")
        else:
            print(f"Error: Word documentation not found at {docx_dir}")
    
    elif format_type == 'pdf':
        # Open PDF documentation in the default PDF viewer
        pdf_dir = os.path.join(docs_dir, 'pdf')
        if os.path.exists(pdf_dir):
            pdf_files = [f for f in os.listdir(pdf_dir) if f.endswith('.pdf')]
            if pdf_files:
                pdf_path = os.path.join(pdf_dir, pdf_files[0])
                if sys.platform == 'win32':
                    os.startfile(pdf_path)
                else:
                    subprocess.run(['xdg-open', pdf_path], check=False)
            else:
                print(f"Error: No .pdf files found in {pdf_dir}")
        else:
            print(f"Error: PDF documentation not found at {pdf_dir}")


def show_installed_packages():
    """
    Show installed packages related to documentation.
    
    This function lists all installed Python packages that are related to
    documentation generation, helping users verify that the required
    dependencies are installed.
    """
    try:
        # Run pip list to get all installed packages
        result = subprocess.run(['pip', 'list'], capture_output=True, text=True, check=True)
        packages = result.stdout.splitlines()
        
        # Filter for documentation-related packages
        doc_related = [
            p for p in packages 
            if any(name in p.lower() for name in ['sphinx', 'doc', 'rst', 'markdown', 'pandoc'])
        ]
        
        if doc_related:
            print("Documentation-related packages installed:")
            for package in doc_related:
                print(f"  {package}")
        else:
            print("No documentation-related packages found")
    except subprocess.CalledProcessError as e:
        print(f"Error checking installed packages: {e}")


def install_dependencies():
    """
    Install required dependencies.
    
    This function installs all the Python packages required for generating
    documentation in various formats. It ensures that all necessary tools
    are available for the documentation workflow.
    """
    # List of required packages with version constraints
    packages = [
        'sphinx>=7.0.0',         # Documentation generator
        'sphinx-rtd-theme>=1.3.0', # Read the Docs theme for Sphinx
        'docxbuilder>=1.2.0',    # Extension for building Word documents
        'markdown>=3.5.0'        # Markdown parser
    ]
    
    try:
        # Install each package using pip
        for package in packages:
            print(f"Installing {package}...")
            subprocess.run(['pip', 'install', package], check=True)
        print("All documentation dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")


def main():
    """
    Main function to parse arguments and run the appropriate command.
    
    This function sets up the command-line interface for the documentation
    workflow tool, parses the arguments, and calls the appropriate functions
    based on the user's commands.
    """
    parser = argparse.ArgumentParser(description='Documentation workflow automation')
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # 'generate' command
    # Used to generate documentation from the codebase
    generate_parser = subparsers.add_parser('generate', help='Generate documentation')
    generate_parser.add_argument('--apps', nargs='+', help='App names to document')
    generate_parser.add_argument(
        '--formats', 
        nargs='+', 
        default=['html', 'docx'], 
        help='Output formats (html, docx, pdf)'
    )
    generate_parser.add_argument(
        '--skip-validation', 
        action='store_true', 
        help='Skip validation step'
    )
    generate_parser.add_argument(
        '--comments-only', 
        action='store_true', 
        help='Only extract from comments, not docstrings'
    )
    generate_parser.add_argument(
        '--markdown-only', 
        action='store_true', 
        help='Only convert markdown files'
    )
    
    # 'open' command
    # Used to open generated documentation
    open_parser = subparsers.add_parser('open', help='Open generated documentation')
    open_parser.add_argument(
        'format', 
        choices=['html', 'docx', 'pdf'], 
        default='html',
        nargs='?',
        help='Documentation format to open'
    )
    
    # 'install' command
    # Used to install documentation dependencies
    install_parser = subparsers.add_parser('install', help='Install documentation dependencies')
    
    # 'info' command
    # Used to display information about the documentation setup
    info_parser = subparsers.add_parser('info', help='Show documentation-related information')
    
    # Parse the arguments
    args = parser.parse_args()
    
    # Validate that we're in a Django project
    validate_project()
    
    # Set up the environment
    setup_environment()
    
    # Execute the appropriate command
    if args.command == 'generate':
        run_autodoc(args)
    elif args.command == 'open':
        open_docs(args.format)
    elif args.command == 'install':
        install_dependencies()
    elif args.command == 'info':
        show_installed_packages()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()