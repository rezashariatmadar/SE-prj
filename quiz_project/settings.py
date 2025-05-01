"""
Django settings for quiz_project project.

This file contains all the configuration for the Django project.
Each setting is documented with explanations of its purpose and potential values.
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# This sets the base directory of the project, making file path handling more robust.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
# This key is used for cryptographic signing. In production, use environment variables.
SECRET_KEY = 'django-insecure-replace-this-with-a-secure-key-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
# Debug mode provides detailed error pages but should be disabled in production.
DEBUG = True

# A list of strings representing the host/domain names that this Django site can serve.
# Required for security when DEBUG = False
ALLOWED_HOSTS = []

# Application definition
# List of all Django applications installed in this project
INSTALLED_APPS = [
    'django.contrib.admin',           # Admin site
    'django.contrib.auth',            # Authentication system
    'django.contrib.contenttypes',    # Content type system
    'django.contrib.sessions',        # Session framework
    'django.contrib.messages',        # Messaging framework
    'django.contrib.staticfiles',     # Static file management
    
    # Third-party apps
    'crispy_forms',                   # Better form rendering
    'crispy_bootstrap4',              # Bootstrap 4 template pack for crispy forms
    'django_extensions',              # Additional Django utilities
    'debug_toolbar',                  # Development debugging toolbar
    
    # Local apps
    'quiz_app',                       # Our quiz application
    'docs',                           # Documentation app with diagrams
]

# Middleware classes - components that process requests/responses
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',            # Security enhancements
    'django.contrib.sessions.middleware.SessionMiddleware',     # Session support
    'django.middleware.common.CommonMiddleware',                # Common features
    'django.middleware.csrf.CsrfViewMiddleware',                # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',     # Messaging support
    'django.middleware.clickjacking.XFrameOptionsMiddleware',   # Clickjacking protection
    'debug_toolbar.middleware.DebugToolbarMiddleware',          # Debug toolbar
]

# The URLconf Python module
ROOT_URLCONF = 'quiz_project.urls'

# Template configuration
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',  # Template engine
        'DIRS': [BASE_DIR / 'templates'],                              # Project-wide templates
        'APP_DIRS': True,                                              # Look for templates in apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',            # Add debug context
                'django.template.context_processors.request',          # Request context
                'django.contrib.auth.context_processors.auth',         # Auth context
                'django.contrib.messages.context_processors.messages', # Messages context
            ],
        },
    },
]

# WSGI application path for production deployment
WSGI_APPLICATION = 'quiz_project.wsgi.application'

# Database configuration
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',   # Database engine
        'NAME': BASE_DIR / 'db.sqlite3',          # Database file path
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/
LANGUAGE_CODE = 'en-us'     # Default language
TIME_ZONE = 'UTC'           # Default timezone
USE_I18N = True             # Internationalization
USE_TZ = True               # Timezone support

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/
STATIC_URL = 'static/'      # URL to use when referring to static files
STATIC_ROOT = BASE_DIR / 'staticfiles'  # Absolute path to collected static files
STATICFILES_DIRS = [        # Additional locations of static files
    BASE_DIR / 'static',
]

# Media files (User-uploaded content)
MEDIA_URL = 'media/'        # URL to use when referring to media files
MEDIA_ROOT = BASE_DIR / 'media'  # Absolute path to media files

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms Configuration
CRISPY_TEMPLATE_PACK = 'bootstrap4'
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap4'

# Debug Toolbar Configuration
INTERNAL_IPS = [
    '127.0.0.1',
]

# Authentication Settings
LOGIN_REDIRECT_URL = 'home'  # After login, redirect to home page
LOGOUT_REDIRECT_URL = 'home'  # After logout, redirect to home page

# Email settings for password reset (for development)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'  # Print emails to console in development 