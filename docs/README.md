# Quiz Game Documentation

This directory contains the comprehensive documentation for the Quiz Game application.

## Building the Documentation

### Prerequisites

- Python 3.8+
- Sphinx and required extensions (installed via `requirements.txt`)

### Build Instructions

#### For Unix/Linux/macOS:

```bash
# Navigate to the docs directory
cd docs

# Build HTML documentation
make html

# Open the documentation in your browser
open _build/html/index.html

# Clean build files
make clean

# Build PDF documentation (requires LaTeX)
make pdf
```

#### For Windows:

```bash
# Navigate to the docs directory
cd docs

# Build HTML documentation
make.bat html

# Open the documentation in your browser
start _build\html\index.html

# Clean build files
make.bat clean

# Build PDF documentation (requires LaTeX)
make.bat latexpdf
```

## Documentation Structure

- **index.rst**: Main entry point and table of contents
- **introduction.rst**: Overview of the application
- **installation.rst**: Installation instructions
- **user_guide.rst**: Guide for end users
- **architecture.rst**: Technical architecture documentation
- **models.rst**: Data model documentation
- **views.rst**: View functions documentation
- **analytics.rst**: Data analysis and visualization documentation
- **_static/**: Directory for images, diagrams and static files

## Generating Diagrams

The project includes scripts to generate diagrams for documentation:

```bash
# Generate ERD diagram
python scripts/generate_erd.py
```

## Documentation Guidelines

When contributing to the documentation:

1. **Consistency**: Maintain consistent formatting and terminology
2. **Clarity**: Write clear, concise explanations
3. **Examples**: Include code examples where appropriate
4. **Screenshots**: Use screenshots to illustrate UI features
5. **SEO**: Use descriptive titles and headings
6. **Links**: Cross-reference related sections
7. **Updates**: Keep documentation in sync with code changes

## Using Sphinx Directives

### Code Blocks

```rst
.. code-block:: python

   def example_function():
       """This is a docstring."""
       return True
```

### Notes and Warnings

```rst
.. note::
   This is an important note!

.. warning::
   This is a warning message!
```

### Cross-References

```rst
See the :doc:`user_guide` for more information.

See the :ref:`specific-section` for details.
```

## Theme Customization

To customize the Sphinx theme, edit `conf.py` and modify the HTML theme options. 