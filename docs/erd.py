"""
Generate a textual Entity Relationship Diagram for the Quiz Game application.

This script analyzes the Django models and creates a textual representation
of the database schema, including tables, fields, and relationships.

What is an ERD?
--------------
An Entity Relationship Diagram (ERD) shows how different data elements in the application
are related to each other. Think of it as a map of the database that shows:
- What kind of information we store (e.g., Users, Questions, Answers)
- How these pieces of information relate to each other (e.g., a User can take many Quizzes)

This script creates a text-based version of this diagram that's easy to read and understand.

Usage:
    python docs/erd.py > docs/_static/database_schema.txt
"""

import os
import sys
import inspect
import django

# Add the parent directory to sys.path so Python can find the quiz_project module
# This is a technical requirement to make the script work properly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")
django.setup()

# Import all the data models we want to include in our diagram
# These are the main "entities" or data types in our application
from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse, UserProfile
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField

def get_model_fields(model):
    """
    Get all fields (properties) for a model, including relationships.
    
    For example, a User model might have fields like:
    - username
    - email
    - password
    - and relationships to other models
    """
    return model._meta.get_fields()

def get_field_type(field):
    """
    Get the field type as a readable string.
    
    This translates technical field types into more understandable formats:
    - ForeignKey: Shows this field connects to another model (e.g., a Question belongs to a Category)
    - OneToOneField: Shows a one-to-one relationship (e.g., each User has exactly one UserProfile)
    - Other field types show what kind of data they store (text, numbers, dates, etc.)
    """
    if isinstance(field, ForeignKey):
        return f"ForeignKey -> {field.related_model.__name__}"
    elif isinstance(field, OneToOneField):
        return f"OneToOneField -> {field.related_model.__name__}"
    elif isinstance(field, ManyToManyField):
        return f"ManyToManyField -> {field.related_model.__name__}"
    else:
        return field.get_internal_type()

def describe_model(model):
    """
    Create a detailed text description of a model and all its fields.
    
    This function:
    1. Prints the model name as a header
    2. Shows the model's description (if available)
    3. Lists all fields with their types, whether they're required, and descriptions
    
    This gives a complete picture of what information this model stores.
    """
    model_name = model.__name__
    fields = get_model_fields(model)
    
    print(f"{'=' * 80}")
    print(f"{model_name} Model")
    print(f"{'-' * 80}")
    
    # Get model docstring if available - this is the description of what this model is for
    if model.__doc__:
        print(f"{model.__doc__.strip()}\n")
    
    print("Fields:")
    print(f"{'-' * 10}")
    
    for field in fields:
        try:
            field_name = field.name
            field_type = get_field_type(field)
            
            # Check if the field has help_text - this explains what the field is for
            help_text = getattr(field, 'help_text', '')
            help_text = f" - {help_text}" if help_text else ''
            
            # Check if field is required - some fields can be left blank, others can't
            required = not getattr(field, 'null', True) and not getattr(field, 'blank', True)
            required_text = " (Required)" if required else ""
            
            print(f"- {field_name}: {field_type}{required_text}{help_text}")
        except AttributeError:
            # Some relation fields might not have all these attributes
            # This handles special cases to avoid errors
            try:
                print(f"- {field.name}: Relation to {field.related_model.__name__}")
            except:
                print(f"- {field}: Special relation field")
    
    print()  # Add a blank line after each model

def describe_analytics():
    """
    Describe the analytics functionality and how it uses the existing data models.
    
    Unlike other features, analytics isn't stored as a separate model in the database.
    Instead, it processes data from existing models to create useful visualizations and insights.
    
    This function explains what the analytics system does and what features it provides.
    """
    print(f"{'=' * 80}")
    print(f"Analytics Functionality")
    print(f"{'-' * 80}")
    print("The analytics system isn't a database model but a feature that analyzes quiz data.")
    print("It provides insights into user performance and learning progress by visualizing quiz results.")
    print("When users view their statistics page, the system processes their quiz history into charts and metrics.\n")
    
    print("Main features:")
    print(f"{'-' * 10}")
    print("- Performance over time tracking: Shows how scores change over multiple quizzes")
    print("- Category-based performance analysis: Compares skills across different subjects")
    print("- Quiz length distribution visualization: Shows what quiz lengths are most common")
    print("- Summary statistics: Calculates averages, identifies strongest categories, and tracks perfect scores")
    print("- Data visualization: Creates charts and graphs using pandas, matplotlib, and seaborn libraries")
    print("\nAll analytics are calculated in real-time when users access their statistics page")
    print("No additional data is stored in the database specifically for analytics")
    print()

def main():
    """
    Generate the complete textual ERD for all models in the quiz application.
    
    This function:
    1. Creates a header for the document
    2. Processes each model to create its description
    3. Adds the analytics functionality description
    4. Summarizes all the relationships between models
    
    The result is a complete picture of the application's data structure.
    """
    print("Entity Relationship Diagram (Text Format)")
    print("=========================================")
    print("Generated on:", django.utils.timezone.now().strftime('%Y-%m-%d %H:%M:%S'))
    print("\nThis document describes the database structure of the Quiz Game application.")
    print("It shows what information is stored and how different parts relate to each other.")
    print()
    
    # User model - first describe the built-in User model that Django provides
    describe_model(User)
    
    # Quiz app models - describe all the custom models specific to our quiz application
    models = [UserProfile, Category, Question, Choice, QuizAttempt, QuizResponse]
    for model in models:
        describe_model(model)
    
    # Describe analytics functionality - this isn't a model but uses the data from models
    describe_analytics()
    
    # Summarize all the relationships between models in a simple format
    # Format: Model A (number) --- (number) Model B, where the numbers show cardinality
    # For example: (1) --- (0-*) means "one to many, where many could be zero"
    print("\nRelationships Summary:")
    print("=====================")
    print("- User (1) --- (0-1) UserProfile: Each user can have one profile")
    print("- User (1) --- (0-*) QuizAttempt: Each user can take many quizzes")
    print("- Category (1) --- (0-*) Question: Each category can have many questions")
    print("- Question (1) --- (0-*) Choice: Each question can have multiple answer choices")
    print("- Category (1) --- (0-*) QuizAttempt: Each quiz belongs to one category")
    print("- QuizAttempt (1) --- (0-*) QuizResponse: Each quiz attempt has multiple question responses")
    print("- Question (1) --- (0-*) QuizResponse: Each response is for one question")
    print("- Choice (1) --- (0-*) QuizResponse: Each response selects one answer choice")
    print("- UserProfile (0-1) --- (0-1) Category: A user can have a favorite category")
    print("- Analytics functionality uses QuizAttempt and QuizResponse data for visualization")

if __name__ == "__main__":
    # This line makes the script run only if executed directly (not when imported)
    main() 