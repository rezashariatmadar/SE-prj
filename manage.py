#!/usr/bin/env python
"""Django's command-line utility for administrative tasks.

This script is the main entry point for Django management commands.
It provides a command-line interface for various tasks, including:
- Running the development server
- Creating migrations
- Applying migrations
- Running tests
- Creating superusers
- And many more built-in and custom management commands

For more information about Django's manage.py, see:
https://docs.djangoproject.com/en/5.0/ref/django-admin/
"""
import os
import sys


def main():
    """
    Run administrative tasks.
    
    This function sets up the Django environment and executes the requested
    management command. It's the main entry point for all Django CLI commands.
    """
    # Set the DJANGO_SETTINGS_MODULE environment variable
    # This tells Django which settings module to use for this project
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
    
    try:
        # Import the execute_from_command_line function from django.core.management
        # This is the function that parses the command line arguments and executes the appropriate command
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # If Django is not installed, show a helpful error message
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    # Execute the command line arguments
    # sys.argv is a list of command-line arguments, with the first item being the script name
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # This block ensures that the script is being run directly and not imported
    # If this script is imported, the main() function won't be executed
    main() 