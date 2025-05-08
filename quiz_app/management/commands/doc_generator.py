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
                try:
                    content += self._generate_form_doc(form)
                except Exception as e:
                    content += f"""
{name}
{'-' * len(name)}

Could not document this form: {str(e)}

"""
        
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
            try:
                # Check field type to handle relationship fields differently
                if hasattr(field, 'get_internal_type'):
                    field_type = field.get_internal_type()
                    help_text = field.help_text if hasattr(field, 'help_text') else 'No description available'
                elif hasattr(field, 'related_model'):
                    # Handle relationship fields
                    if hasattr(field, 'field'):
                        # ManyToManyRel
                        field_type = f"Relationship (Many-to-Many) to {field.related_model.__name__}"
                    elif hasattr(field, 'remote_field'):
                        # ManyToOneRel (reverse ForeignKey)
                        field_type = f"Relationship (Reverse Foreign Key) to {field.related_model.__name__}"
                    else:
                        field_type = f"Relationship to {field.related_model.__name__}"
                    help_text = 'Relationship field - see model documentation'
                else:
                    field_type = field.__class__.__name__
                    help_text = 'No description available'

                content += f"""
{field.name}
    Type: {field_type}
    Description: {help_text}
"""
            except Exception as e:
                # Fail gracefully if we can't document a field
                content += f"""
{field.name if hasattr(field, 'name') else 'Unknown field'}
    Type: Unknown
    Description: Could not document this field - {str(e)}
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
        
        content = f"""
{form.__name__}
{'-' * len(form.__name__)}

{self._format_docstring(docstring)}

"""
        
        # Try to get fields - this might fail for form classes that don't have
        # fields defined as class attributes (they might be defined in __init__)
        try:
            # For Django form instances, fields are instance attributes
            if hasattr(form, 'fields'):
                # Direct access to fields (form instance)
                fields = form.fields
                content += """
Fields
~~~~~~

"""
                for name, field in fields.items():
                    help_text = field.help_text if hasattr(field, 'help_text') else 'No description available'
                    required = field.required if hasattr(field, 'required') else 'Unknown'
                    content += f"""
{name}
    Type: {field.__class__.__name__}
    Required: {required}
    Description: {help_text}
"""
            # For form classes (not instances), try to create an instance
            elif hasattr(form, 'declared_fields'):
                fields = form.declared_fields
                content += """
Fields
~~~~~~

"""
                for name, field in fields.items():
                    help_text = field.help_text if hasattr(field, 'help_text') else 'No description available'
                    required = field.required if hasattr(field, 'required') else 'Unknown'
                    content += f"""
{name}
    Type: {field.__class__.__name__}
    Required: {required}
    Description: {help_text}
"""
            # Try to create an instance if it's a class
            elif inspect.isclass(form) and hasattr(form, '__init__'):
                try:
                    # Try to create an instance - this might fail if form requires parameters
                    instance = form()
                    if hasattr(instance, 'fields'):
                        fields = instance.fields
                        content += """
Fields
~~~~~~

"""
                        for name, field in fields.items():
                            help_text = field.help_text if hasattr(field, 'help_text') else 'No description available'
                            required = field.required if hasattr(field, 'required') else 'Unknown'
                            content += f"""
{name}
    Type: {field.__class__.__name__}
    Required: {required}
    Description: {help_text}
"""
                except Exception:
                    content += """
Fields
~~~~~~

Could not instantiate form to get field information. Fields might be defined in __init__ or require parameters.
"""
            else:
                content += """
Fields
~~~~~~

Could not determine fields for this form.
"""
        except Exception as e:
            content += f"""
Fields
~~~~~~

Error retrieving fields: {str(e)}
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