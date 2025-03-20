"""Template definitions for documentation files."""

TEMPLATES = {
    'api': """{title}
{'=' * len(title)}

Last updated: {date}

Overview
--------
{overview}

Endpoints
---------
{endpoints}

Authentication
-------------
{authentication}

Error Handling
-------------
{error_handling}

Examples
--------
{examples}
""",

    'model': """{title}
{'=' * len(title)}

Last updated: {date}

Model Overview
-------------
{overview}

Fields
------
{fields}

Methods
-------
{methods}

Relationships
------------
{relationships}

Usage Examples
-------------
{examples}
""",

    'view': """{title}
{'=' * len(title)}

Last updated: {date}

View Overview
------------
{overview}

URL Pattern
----------
{url_pattern}

Context Data
-----------
{context_data}

Template
--------
{template}

Example Usage
------------
{examples}
""",

    'form': """{title}
{'=' * len(title)}

Last updated: {date}

Form Overview
------------
{overview}

Fields
------
{fields}

Validation
----------
{validation}

Usage Example
------------
{examples}
"""
} 