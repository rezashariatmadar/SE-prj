Documentation Workflow Guide
==========================

Last updated: 2024-03-20

This document provides instructions for using the automated documentation workflow script.

Overview
--------

The documentation workflow script automates the entire documentation process, from validation to building final documents in multiple formats. It combines several steps into a single command:

1. Validates existing documentation
2. Generates documentation from Python docstrings
3. Converts Markdown files to RST format
4. Extracts documentation from code comments
5. Builds documentation in various formats (HTML, LaTeX, PDF, Word)

Prerequisites
------------

To use the documentation workflow script, you need:

1. Python 3.7+
2. Django
3. Sphinx and extensions:

   .. code-block:: bash

       pip install sphinx sphinx-rtd-theme docxbuilder

4. For Markdown conversion:

   .. code-block:: bash

       pip install pypandoc

5. For PDF output:
   
   - Windows: MiKTeX (https://miktex.org/)
   - Linux: ``apt-get install texlive-full``
   - macOS: MacTeX (https://www.tug.org/mactex/)

Usage
-----

Basic Usage
~~~~~~~~~~

To run the full workflow:

.. code-block:: bash

    python docs/docs_workflow.py

This will run all steps of the workflow and generate documentation in all supported formats.

Selective Steps
~~~~~~~~~~~~~~

You can select which steps to run using the ``--skip-*`` arguments:

.. code-block:: bash

    python docs/docs_workflow.py --skip-validation --skip-md-conversion

Available skip options:

* ``--skip-validation``: Skip documentation validation
* ``--skip-generation``: Skip docstring documentation generation
* ``--skip-md-conversion``: Skip Markdown conversion
* ``--skip-comments``: Skip code comment extraction
* ``--skip-build``: Skip documentation building

Specific Output Formats
~~~~~~~~~~~~~~~~~~~~~~

To generate only specific output formats:

.. code-block:: bash

    python docs/docs_workflow.py --output-format html

Available formats:

* ``html``: HTML documentation
* ``latex``: LaTeX source files
* ``pdf``: PDF document (requires LaTeX)
* ``word``: Microsoft Word document
* ``all``: All formats (default)

Specific Applications
~~~~~~~~~~~~~~~~~~~

To generate documentation for specific Django apps:

.. code-block:: bash

    python docs/docs_workflow.py --apps quiz_app user_app

Output Locations
--------------

The script generates documentation in these locations:

* HTML: ``docs/_build/html/index.html``
* Word: ``docs/_build/docx/QuizGame.docx``
* LaTeX: ``docs/_build/latex/*.tex``
* PDF: ``docs/_build/latex/*.pdf``

Advanced Usage
-------------

Automated Documentation in CI/CD
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can integrate the documentation workflow in your CI/CD pipeline:

.. code-block:: yaml

    documentation:
      stage: build
      script:
        - pip install -r requirements.txt
        - python docs/docs_workflow.py
      artifacts:
        paths:
          - docs/_build/

Custom Documentation Comments
~~~~~~~~~~~~~~~~~~~~~~~~~~~

To include code comments in documentation, use these formats:

Python:
    Triple-quoted docstrings.

JavaScript:
    .. code-block:: javascript

        // @doc This will be included in documentation

CSS:
    .. code-block:: css

        /** This will be included in documentation */

HTML:
    .. code-block:: html

        <!-- @doc This will be included in documentation -->

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~

1. **Missing docxbuilder**

   .. code-block:: bash

       pip install docxbuilder

2. **pypandoc errors**

   Make sure you have pandoc installed on your system:
   
   - Windows: ``choco install pandoc``
   - macOS: ``brew install pandoc``
   - Linux: ``apt-get install pandoc``

3. **PDF generation fails**

   Ensure you have a LaTeX distribution installed and the ``pdflatex`` command is available.

4. **Import errors**

   Ensure you run the script from the project root directory where ``manage.py`` is located. 