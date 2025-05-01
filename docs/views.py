from django.shortcuts import render
from django.views.generic import TemplateView

class DiagramsView(TemplateView):
    """View for displaying the project diagrams."""
    template_name = 'docs/diagrams.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Add diagram categories and counts
        context['diagram_categories'] = [
            {
                'name': 'Data Flow Diagrams',
                'count': 3,
                'icon': 'fa-project-diagram',
                'id': 'dfd-diagrams'
            },
            {
                'name': 'Use Case Diagram',
                'count': 1,
                'icon': 'fa-users',
                'id': 'use-case'
            },
            {
                'name': 'Sequence Diagram',
                'count': 1,
                'icon': 'fa-exchange-alt',
                'id': 'sequence'
            },
            {
                'name': 'Component Diagram',
                'count': 1,
                'icon': 'fa-puzzle-piece',
                'id': 'component'
            },
            {
                'name': 'Project Planning',
                'count': 3,
                'icon': 'fa-tasks',
                'id': 'project-planning'
            }
        ]
        
        return context 