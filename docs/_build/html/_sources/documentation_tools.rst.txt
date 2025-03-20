Documentation Automation Tools
=============================

Last updated: 2024-03-20

This document describes the documentation automation tools available in this project.

Overview
--------

The project includes a comprehensive documentation automation system that helps maintain high-quality documentation with minimal effort. The system provides tools for:

1. Creating and managing documentation files
2. Using pre-defined templates for consistent formatting
3. Validating documentation against best practices
4. Automatically generating documentation from source code
5. Converting between different documentation formats

Management Command
-----------------

The primary interface for documentation automation is the ``manage_docs`` Django management command:

.. code-block:: bash

    python manage.py manage_docs [action] [options]

Available actions:

* ``create`` - Create a new documentation file
* ``update`` - Update an existing documentation file
* ``delete`` - Delete a documentation file
* ``generate`` - Generate documentation from source code
* ``validate`` - Validate documentation files

Templates
---------

The system includes several pre-defined templates for common documentation types:

* ``api`` - Template for API documentation
* ``model`` - Template for model documentation
* ``view`` - Template for view documentation
* ``form`` - Template for form documentation

To create a file using a template:

.. code-block:: bash

    python manage.py manage_docs create --file api_docs --title "API Documentation" --template api

Each template includes appropriate sections and placeholders for the specific type of documentation.

Validation
----------

The system can validate documentation files against best practices:

.. code-block:: bash

    python manage.py manage_docs validate

This checks for:

* Proper RST formatting
* Correct section underlines
* Broken documentation links
* Missing code examples
* Invalid image paths

You can also validate a single file during creation or update:

.. code-block:: bash

    python manage.py manage_docs update --file api_docs --content "New content" --validate

Automatic Generation
-------------------

The system can generate documentation from source code docstrings:

.. code-block:: bash

    python manage.py manage_docs generate --app quiz_app

This analyzes Python docstrings in models, views, and forms to create comprehensive documentation files. The generator:

* Extracts class and method docstrings
* Formats them appropriately for RST
* Creates structured documentation with proper sections
* Includes field information, parameters, and return values

Usage Examples
-------------

Creating a new documentation file:

.. code-block:: bash

    python manage.py manage_docs create --file advanced_usage --title "Advanced Usage Guide" --content "Initial content"

Adding content to a specific section:

.. code-block:: bash

    python manage.py manage_docs update --file advanced_usage --section "Configuration" --content "Configuration details here"

Generating model documentation:

.. code-block:: bash

    python manage.py manage_docs generate --app quiz_app --validate

Deleting a documentation file:

.. code-block:: bash

    python manage.py manage_docs delete --file outdated_doc

Implementation Details
---------------------

The documentation system consists of several components:

* ``manage_docs.py`` - Main management command
* ``doc_templates.py`` - Template definitions
* ``doc_validator.py`` - Documentation validation
* ``doc_generator.py`` - Automatic documentation generation

These components work together to provide a seamless documentation workflow. 