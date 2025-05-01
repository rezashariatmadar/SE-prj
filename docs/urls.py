from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import DiagramsView

app_name = 'docs'

urlpatterns = [
    path('diagrams/', DiagramsView.as_view(), name='diagrams'),
]

# Serve static files from docs/diagrams/static
if settings.DEBUG:
    urlpatterns += static('/docs/diagrams/static/', document_root=settings.BASE_DIR / 'docs/diagrams/static/') 