"""
ASGI config for quiz_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

This file is used by ASGI-compatible web servers to serve the application in a production
environment. ASGI (Asynchronous Server Gateway Interface) is the spiritual successor
to WSGI, designed to provide a standard interface between async-capable web servers
and both synchronous and asynchronous web applications.

ASGI provides support for:
- WebSockets
- HTTP/2
- Background tasks
- Other async protocols alongside traditional HTTP

Common ASGI servers that can use this file include:
- Daphne
- Uvicorn
- Hypercorn

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# Set the default Django settings module for the ASGI application
# This ensures that the application knows which settings to use
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')

# Get the ASGI application object that web servers will use
application = get_asgi_application() 