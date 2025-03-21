"""
Generate a textual Entity Relationship Diagram for the Quiz Game application.

This script analyzes the Django models and creates a textual representation
of the database schema, including tables, fields, and relationships.

Usage:
    python docs/erd.py > docs/_static/database_schema.txt
"""

import os
import sys
import inspect
import django

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")
django.setup()

# Import the models
from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse, UserProfile
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField

def get_model_fields(model):
    """Get all fields for a model, including relationships."""
    return model._meta.get_fields()

def get_field_type(field):
    """Get the field type as a string."""
    if isinstance(field, ForeignKey):
        return f"ForeignKey -> {field.related_model.__name__}"
    elif isinstance(field, OneToOneField):
        return f"OneToOneField -> {field.related_model.__name__}"
    elif isinstance(field, ManyToManyField):
        return f"ManyToManyField -> {field.related_model.__name__}"
    else:
        return field.get_internal_type()

def describe_model(model):
    """Describe a model and its fields."""
    model_name = model.__name__
    fields = get_model_fields(model)
    
    print(f"{'=' * 80}")
    print(f"{model_name} Model")
    print(f"{'-' * 80}")
    
    # Get model docstring if available
    if model.__doc__:
        print(f"{model.__doc__.strip()}\n")
    
    print("Fields:")
    print(f"{'-' * 10}")
    
    for field in fields:
        try:
            field_name = field.name
            field_type = get_field_type(field)
            
            # Check if the field has help_text
            help_text = getattr(field, 'help_text', '')
            help_text = f" - {help_text}" if help_text else ''
            
            # Check if field is required
            required = not getattr(field, 'null', True) and not getattr(field, 'blank', True)
            required_text = " (Required)" if required else ""
            
            print(f"- {field_name}: {field_type}{required_text}{help_text}")
        except AttributeError:
            # Some relation fields might not have all these attributes
            try:
                print(f"- {field.name}: Relation to {field.related_model.__name__}")
            except:
                print(f"- {field}: Special relation field")
    
    print()  # Add a blank line after each model

def main():
    """Generate textual ERD for all models."""
    print("Entity Relationship Diagram (Text Format)")
    print("=========================================")
    print("Generated on:", django.utils.timezone.now().strftime("%Y-%m-%d %H:%M:%S"))
    print()
    
    # User model
    describe_model(User)
    
    # Quiz app models
    models = [UserProfile, Category, Question, Choice, QuizAttempt, QuizResponse]
    for model in models:
        describe_model(model)
    
    print("\nRelationships Summary:")
    print("=====================")
    print("- User (1) --- (0-1) UserProfile")
    print("- User (1) --- (0-*) QuizAttempt")
    print("- Category (1) --- (0-*) Question")
    print("- Question (1) --- (0-*) Choice")
    print("- Category (1) --- (0-*) QuizAttempt")
    print("- QuizAttempt (1) --- (0-*) QuizResponse")
    print("- Question (1) --- (0-*) QuizResponse")
    print("- Choice (1) --- (0-*) QuizResponse")
    print("- UserProfile (0-1) --- (0-1) Category (favorite)")

if __name__ == "__main__":
    main() 