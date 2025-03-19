#!/usr/bin/env python
"""
Generate Entity Relationship Diagram for the Quiz Game application.

This script uses django-extensions and pygraphviz to create an ERD diagram
of the application's models. The diagram is saved to the docs/_static directory.

Requirements:
- django-extensions
- pygraphviz
- pydot

Usage:
    python scripts/generate_erd.py
"""

import os
import sys
import django
from django.core.management import call_command

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

# Directory where the ERD will be saved
output_dir = os.path.join('docs', '_static')
output_file = os.path.join(output_dir, 'erd_diagram')

# Create output directory if it doesn't exist
os.makedirs(output_dir, exist_ok=True)

# Generate the ERD
try:
    print(f"Generating ERD diagram to {output_file}.png...")
    call_command(
        'graph_models',
        'quiz_app',
        'auth',
        output=output_file,
        format='png',
        layout='dot',
        theme='django2018',
        group_models=True,
        exclude_models='ContentType,Permission,Session',
        verbosity=1
    )
    print("ERD generation complete!")
except Exception as e:
    print(f"Error generating ERD: {e}")
    print("\nMake sure you have installed:")
    print("- django-extensions")
    print("- pygraphviz (requires graphviz system package)")
    print("- pydot")
    sys.exit(1)

# Generate a simplified version showing just the quiz app models
try:
    print(f"Generating simplified ERD diagram to {output_file}_simple.png...")
    call_command(
        'graph_models',
        'quiz_app',
        output=f"{output_file}_simple",
        format='png',
        layout='dot',
        theme='django2018',
        verbosity=1
    )
    print("Simplified ERD generation complete!")
except Exception as e:
    print(f"Error generating simplified ERD: {e}")
    sys.exit(1)

print("\nERD diagrams have been generated. You can now include them in your documentation.")
print(f"- Full ERD: {output_file}.png")
print(f"- Simple ERD: {output_file}_simple.png")
print("\nTo include in RST files:")
print(".. image:: _static/erd_diagram.png")
print("   :alt: Entity Relationship Diagram")
print("   :align: center")
print("   :width: 600px") 