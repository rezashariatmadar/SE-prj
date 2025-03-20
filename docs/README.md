# Quiz Game Documentation

This directory contains the comprehensive documentation for the Quiz Game application.

## Building the Documentation

### Prerequisites

- Python 3.8+
- Sphinx and required extensions (installed via `requirements.txt`)
- For automated documentation workflow: `docxbuilder` and `pypandoc`
- For PDF output: LaTeX (MiKTeX on Windows, MacTeX on macOS, texlive on Linux)

### Build Instructions

#### Using the Automated Documentation Workflow

The easiest way to build documentation is using our automated workflow script:

```bash
# Generate all documentation formats
python docs/docs_workflow.py

# Generate only Word documentation
python docs/docs_workflow.py --output-format word

# Generate only HTML documentation
python docs/docs_workflow.py --output-format html

# Skip specific steps
python docs/docs_workflow.py --skip-validation --skip-md-conversion
```

#### Manual Build (For Unix/Linux/macOS):

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

# Build Word documentation
make docx
```

#### Manual Build (For Windows):

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

# Build Word documentation
make.bat docx
```

## Documentation Management

The project includes a Django management command for managing documentation:

```bash
# Create a new documentation file
python manage.py manage_docs create --file new_doc --title "New Document"

# Create a new documentation file with template
python manage.py manage_docs create --file api_docs --title "API Documentation" --template api

# Update existing documentation
python manage.py manage_docs update --file existing_file --section "New Section" --content "Content here"

# Delete documentation
python manage.py manage_docs delete --file outdated_doc

# Generate documentation from source code
python manage.py manage_docs generate --app quiz_app

# Validate documentation
python manage.py manage_docs validate
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
- **documentation_tools.rst**: Documentation about the documentation tools
- **documentation_workflow.rst**: Guide for using the documentation workflow
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

## Custom Documentation Comments

To include code comments in documentation, use these formats:

### Python
Triple-quoted docstrings are automatically extracted.

### JavaScript
```javascript
// @doc This will be included in documentation
```

### CSS
```css
/** This will be included in documentation */
```

### HTML
```html
<!-- @doc This will be included in documentation -->
``` 