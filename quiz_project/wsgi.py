"""
WSGI config for quiz_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

This file is used by WSGI-compatible web servers to serve the application in a production
environment. WSGI (Web Server Gateway Interface) is the standard interface between web
server software and web applications written in Python.

Common WSGI servers that can use this file include:
- Gunicorn
- uWSGI
- mod_wsgi (with Apache)

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

# Set the default Django settings module for the WSGI application
# This ensures that the application knows which settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

# Get the WSGI application object that web servers will use
application = get_wsgi_application() 