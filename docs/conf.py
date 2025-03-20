"""
Configuration file for the Sphinx documentation builder.

This file contains all configuration needed to generate the documentation
for the Quiz Game project.
"""

import os
import sys
import django

# Add project root to sys.path
sys.path.insert(0, os.path.abspath('..'))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

# Project information
project = 'Quiz Game'
copyright = '2024, Your Name'
author = 'Your Name'
release = '1.0.0'

# General configuration
extensions = [
    'sphinx.ext.autodoc',          # Auto-generate documentation from docstrings
    'sphinx.ext.viewcode',         # Add links to source code
    'sphinx.ext.napoleon',         # Support for NumPy and Google style docstrings
    'sphinx.ext.intersphinx',      # Generate links to other documentation
    'sphinx.ext.todo',             # Support for todo items
    'sphinx.ext.coverage',         # Check documentation coverage
    'sphinx.ext.mathjax',          # Render math via MathJax
    'sphinx_rtd_theme',            # Read the Docs theme
    'docxbuilder',                 # Docx builder
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', 'venv']

# Options for HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_title = 'Quiz Game Documentation'

# Options for autodoc extension
autodoc_member_order = 'bysource'
autodoc_typehints = 'description'
autoclass_content = 'both'

# Options for intersphinx extension
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'django': ('https://docs.djangoproject.com/en/stable/', None),
    'pandas': ('https://pandas.pydata.org/pandas-docs/stable/', None),
    'matplotlib': ('https://matplotlib.org/stable/', None),
}

# Options for napoleon extension
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_use_keyword = True
napoleon_custom_sections = None

# Options for todo extension
todo_include_todos = True 