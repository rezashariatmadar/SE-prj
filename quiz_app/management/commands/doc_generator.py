"""Automatic documentation generator from docstrings."""

import os
import inspect
import importlib
from datetime import datetime
from typing import List, Dict, Any
from django.apps import apps
from .doc_validator import DocValidator

class DocGenerator:
    """Generates documentation from Python docstrings."""

    def __init__(self):
        self.validator = DocValidator()

    def generate_model_docs(self, app_name: str) -> str:
        """Generate documentation for models in an app."""
        app_config = apps.get_app_config(app_name)
        models = app_config.get_models()
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        content = f"""Models
{'=' * 6}

Last updated: {current_date}

This document describes all models in the {app_name} application.

"""
        
        for model in models:
            content += self._generate_model_doc(model)
        
        return content

    def generate_view_docs(self, app_name: str) -> str:
        """Generate documentation for views in an app."""
        app_config = apps.get_app_config(app_name)
        views_module = importlib.import_module(f'{app_name}.views')
        views = inspect.getmembers(views_module, inspect.isclass)
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        content = f"""Views
{'=' * 5}

Last updated: {current_date}

This document describes all views in the {app_name} application.

"""
        
        for name, view in views:
            if name.endswith('View'):
                content += self._generate_view_doc(view)
        
        return content

    def generate_form_docs(self, app_name: str) -> str:
        """Generate documentation for forms in an app."""
        app_config = apps.get_app_config(app_name)
        forms_module = importlib.import_module(f'{app_name}.forms')
        forms = inspect.getmembers(forms_module, inspect.isclass)
        
        current_date = datetime.now().strftime('%Y-%m-%d')
        content = f"""Forms
{'=' * 5}

Last updated: {current_date}

This document describes all forms in the {app_name} application.

"""
        
        for name, form in forms:
            if name.endswith('Form'):
                content += self._generate_form_doc(form)
        
        return content

    def _generate_model_doc(self, model) -> str:
        """Generate documentation for a single model."""
        docstring = inspect.getdoc(model) or ''
        fields = model._meta.get_fields()
        
        content = f"""
{model.__name__}
{'-' * len(model.__name__)}

{self._format_docstring(docstring)}

Fields
~~~~~~

"""
        
        for field in fields:
            content += f"""
{field.name}
    Type: {field.get_internal_type()}
    Description: {field.help_text or 'No description available'}
"""
        
        # Add methods
        methods = inspect.getmembers(model, inspect.isfunction)
        if methods:
            content += """
Methods
~~~~~~~
"""
            for name, method in methods:
                if not name.startswith('_'):
                    method_doc = inspect.getdoc(method) or ''
                    content += f"""
{name}
    {self._format_docstring(method_doc)}
"""
        
        return content

    def _generate_view_doc(self, view) -> str:
        """Generate documentation for a single view."""
        docstring = inspect.getdoc(view) or ''
        
        content = f"""
{view.__name__}
{'-' * len(view.__name__)}

{self._format_docstring(docstring)}

"""
        
        # Add URL pattern if available
        if hasattr(view, 'url_pattern'):
            content += f"""
URL Pattern
~~~~~~~~~~
{view.url_pattern}
"""
        
        # Add template if available
        if hasattr(view, 'template_name'):
            content += f"""
Template
~~~~~~~~
{view.template_name}
"""
        
        return content

    def _generate_form_doc(self, form) -> str:
        """Generate documentation for a single form."""
        docstring = inspect.getdoc(form) or ''
        fields = form.fields
        
        content = f"""
{form.__name__}
{'-' * len(form.__name__)}

{self._format_docstring(docstring)}

Fields
~~~~~~

"""
        
        for name, field in fields.items():
            content += f"""
{name}
    Type: {field.__class__.__name__}
    Required: {field.required}
    Description: {field.help_text or 'No description available'}
"""
        
        return content

    def _format_docstring(self, docstring: str) -> str:
        """Format docstring for RST output."""
        if not docstring:
            return "No documentation available."
        
        # Convert Google-style docstrings to RST
        lines = docstring.split('\n')
        formatted_lines = []
        
        for line in lines:
            if line.strip().startswith('Args:'):
                formatted_lines.append('\nParameters\n~~~~~~~~~')
            elif line.strip().startswith('Returns:'):
                formatted_lines.append('\nReturns\n~~~~~~~~')
            elif line.strip().startswith('Raises:'):
                formatted_lines.append('\nRaises\n~~~~~~')
            else:
                formatted_lines.append(line)
        
        return '\n'.join(formatted_lines)

    def generate_all_docs(self, app_name: str) -> Dict[str, str]:
        """Generate all documentation for an app."""
        return {
            'models': self.generate_model_docs(app_name),
            'views': self.generate_view_docs(app_name),
            'forms': self.generate_form_docs(app_name)
        } 