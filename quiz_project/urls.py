"""
URL Configuration for quiz_project.

This module defines the URL patterns for the entire project.
It includes paths for:
- Admin interface
- Quiz application routes
- Static and media file serving in development
- Debug toolbar (when in DEBUG mode)
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views  # Import authentication views

urlpatterns = [
    # Admin site
    path('admin/', admin.site.urls, name='admin'),
    
    # Quiz application URLs
    path('quiz/', include('quiz_app.urls')),
    
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Include all authentication URLs (password reset, change, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Redirect root URL to quiz app
    path('', RedirectView.as_view(pattern_name='quiz:index'), name='home'),
]

# Add debug toolbar URLs in development mode
if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 