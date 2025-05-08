"""
Generate a visual Entity Relationship Diagram for the Quiz Game application.

This script uses the graphviz Python library to create a visual representation
of the database schema, including tables and relationships.

Usage:
    python docs/generate_visual_erd.py
"""

import os
import sys
import django
from graphviz import Digraph

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")
django.setup()

# Import the models
from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse, UserProfile
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField


def get_model_fields(model):
    """Get all fields for a model, excluding relations."""
    return [f for f in model._meta.get_fields() if not f.is_relation]


def get_relation_fields(model):
    """Get relation fields for a model."""
    fields = model._meta.get_fields()
    return [f for f in fields if f.is_relation]


def create_erd():
    """Create the ERD diagram."""
    # Create the graph
    dot = Digraph(comment='Quiz Game Entity Relationship Diagram')
    dot.attr(rankdir='LR', size='8,5')
    dot.attr('node', shape='record', style='filled', fillcolor='lightblue')

    # Define the models to include
    models = [User, UserProfile, Category, Question, Choice, QuizAttempt, QuizResponse]
    
    # Add nodes for each model
    for model in models:
        model_name = model.__name__
        
        # Get regular fields
        fields = get_model_fields(model)
        field_str = '\\n'.join([f.name + ': ' + f.get_internal_type() for f in fields])
        
        # Create node label with model name and fields
        label = f"{{{model_name}|{field_str}}}"
        dot.node(model_name, label)

    # Add Analytics as a virtual entity
    analytics_node = "Analytics"
    analytics_fields = "performance_time\\ncategory_performance\\nquestion_distribution\\nsummary_statistics"
    analytics_label = f"{{{analytics_node}|{analytics_fields}}}"
    dot.attr('node', shape='record', style='filled', fillcolor='#FFC0CB')  # Light pink
    dot.node(analytics_node, analytics_label)
    
    # Add edges for relationships
    edges = [
        # User relationships
        (User, UserProfile, 'one-to-one', '1', '0..1'),
        (User, QuizAttempt, 'one-to-many', '1', '0..*'),
        
        # Category relationships
        (Category, Question, 'one-to-many', '1', '0..*'),
        (Category, QuizAttempt, 'one-to-many', '1', '0..*'),
        (Category, UserProfile, 'one-to-many', '1', '0..*'),
        
        # Question relationships
        (Question, Choice, 'one-to-many', '1', '0..*'),
        (Question, QuizResponse, 'one-to-many', '1', '0..*'),
        
        # QuizAttempt relationships
        (QuizAttempt, QuizResponse, 'one-to-many', '1', '0..*'),
        
        # Choice relationships
        (Choice, QuizResponse, 'one-to-many', '1', '0..*'),
    ]
    
    # Add edges
    for source, target, rel_type, source_label, target_label in edges:
        source_name = source.__name__
        target_name = target.__name__
        
        if rel_type == 'one-to-one':
            dot.edge(source_name, target_name, label=f"{source_label}:{target_label}", dir='both', arrowtail='none', arrowhead='none')
        elif rel_type == 'one-to-many':
            dot.edge(source_name, target_name, label=f"{source_label}:{target_label}", dir='forward')

    # Add Analytics virtual relationships (dashed lines)
    dot.attr('edge', style='dashed')
    dot.edge("QuizAttempt", analytics_node, label="data source", dir='forward')
    dot.edge("QuizResponse", analytics_node, label="data source", dir='forward')
    dot.edge("User", analytics_node, label="views", dir='forward')
    
    # Create directory if it doesn't exist
    os.makedirs('docs/_static', exist_ok=True)
    
    # Render the graph
    dot.render('docs/_static/erd_diagram', format='png', cleanup=True)
    print("ERD diagram has been generated at docs/_static/erd_diagram.png")


if __name__ == "__main__":
    create_erd() 