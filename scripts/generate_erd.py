#!/usr/bin/env python
"""
Generate an Entity Relationship Diagram for the Quiz application models using matplotlib.

This script creates a visual representation of the database relationships between models
in the quiz application. It uses matplotlib to draw boxes for each model and arrows
for the relationships between them.

Usage:
    python scripts/generate_erd.py
"""

import os
import sys
import django
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch

# Set up Django environment
# This allows the script to access Django models outside of the main application
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.apps import apps
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField

# Get all models from the quiz_app
# This retrieves all model classes defined in the quiz_app application
app_models = apps.get_app_config('quiz_app').get_models()

# Create a figure
# The figure size is set to 16x12 inches for a large, detailed diagram
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Hide axes
# We don't need coordinate axes for this diagram
ax.axis('off')

# Define colors
# These colors define the visual theme of the diagram
model_color = '#E5F5E0'    # Light green background for model boxes
border_color = '#31a354'    # Darker green for borders
header_color = '#A1D99B'    # Medium green for header section
title_color = '#006D2C'     # Dark green for model names
arrow_color = '#636363'     # Gray for relationship arrows

# Calculate positions based on number of models
# These settings control the layout and spacing of model boxes
model_width = 18            # Width of each model box
model_height = 0            # Will be calculated based on fields
model_padding = 5           # Padding between model boxes
models_per_row = 3          # Number of models to display in each row
horizontal_spacing = (100 - (models_per_row * model_width)) / (models_per_row + 1)

# Dictionaries to store model positions and relationship data
model_positions = {}        # Stores the position and size of each model box
relation_arrows = []        # Stores information about relationship arrows

# Arrange models in a grid
# This section calculates the position of each model box in the diagram
row = 0
col = 0
max_height_in_row = 0
vertical_position = 90      # Start from top

for i, model in enumerate(sorted(app_models, key=lambda m: m.__name__)):
    # Calculate height based on number of fields
    # Each model's height depends on how many fields it contains
    fields = model._meta.get_fields()
    field_height = 1.5      # Height for each field
    header_height = 3       # Height for the header section
    model_height = header_height + (len(fields) * field_height)
    
    # Adjust position if we need a new row
    # Start a new row when we've filled the current row with models
    if col >= models_per_row:
        col = 0
        row += 1
        vertical_position -= max_height_in_row + model_padding
        max_height_in_row = 0
    
    # Calculate position
    # Determine the x,y coordinates for this model box
    x = horizontal_spacing + col * (model_width + horizontal_spacing)
    y = vertical_position - model_height
    
    # Store position for relationships
    # Save the model's position and field information for drawing arrows later
    model_positions[model] = {
        'x': x, 
        'y': y, 
        'width': model_width, 
        'height': model_height,
        'fields': {f.name: i for i, f in enumerate(fields)}
    }
    
    # Update max height in row
    # Keep track of the tallest model in this row for vertical spacing
    max_height_in_row = max(max_height_in_row, model_height)
    
    # Draw model box
    # Create and add the rectangle representing the model
    rect = Rectangle((x, y), model_width, model_height, 
                    facecolor=model_color, edgecolor=border_color, lw=1)
    ax.add_patch(rect)
    
    # Draw header
    # Create and add the rectangle for the model name header section
    header_rect = Rectangle((x, y + model_height - header_height), model_width, header_height, 
                           facecolor=header_color, edgecolor=border_color, lw=1)
    ax.add_patch(header_rect)
    
    # Add model name
    # Display the model's name in the header section
    ax.text(x + model_width/2, y + model_height - header_height/2, model.__name__, 
            ha='center', va='center', fontsize=12, fontweight='bold', color=title_color)
    
    # Add fields
    # List each field of the model with relationship indicators
    for j, field in enumerate(fields):
        field_y = y + model_height - header_height - (j + 1) * field_height + field_height/2
        field_text = field.name
        
        # Identify field type for relationships
        # Add arrows based on the type of relationship (FK, O2O, M2M)
        if isinstance(field, ForeignKey):
            field_text += f' → {field.related_model.__name__}'  # Arrow indicating ForeignKey
            relation_arrows.append({
                'from_model': model,
                'from_field': field.name,
                'to_model': field.related_model,
                'type': 'FK'
            })
        elif isinstance(field, OneToOneField):
            field_text += f' ↔ {field.related_model.__name__}'  # Double arrow for OneToOne
            relation_arrows.append({
                'from_model': model,
                'from_field': field.name,
                'to_model': field.related_model,
                'type': 'O2O'
            })
        elif isinstance(field, ManyToManyField):
            field_text += f' ⇆ {field.related_model.__name__}'  # Double arrow with bars for ManyToMany
            relation_arrows.append({
                'from_model': model,
                'from_field': field.name,
                'to_model': field.related_model,
                'type': 'M2M'
            })
            
        ax.text(x + 0.5, field_y, field_text, fontsize=10, va='center')
    
    # Increment column
    # Move to the next horizontal position for the next model
    col += 1

# Draw relationship arrows
# This section creates arrows between models based on their relationships
for rel in relation_arrows:
    if rel['to_model'] in model_positions and rel['from_model'] in model_positions:
        from_pos = model_positions[rel['from_model']]
        to_pos = model_positions[rel['to_model']]
        
        # Calculate arrow positions
        # Determine where the arrow should start and end
        from_field_idx = from_pos['fields'].get(rel['from_field'], 0)
        from_y = from_pos['y'] + from_pos['height'] - 3 - (from_field_idx + 1) * 1.5 + 1.5/2
        
        # Start and end positions
        start_x = from_pos['x'] + from_pos['width']
        start_y = from_y
        end_x = to_pos['x']
        end_y = to_pos['y'] + to_pos['height'] - 1.5  # Point to top of model
        
        # Draw arrow based on relationship type
        # Use different arrow styles for different relationship types
        if rel['type'] == 'FK':
            # Single arrow for ForeignKey (one-to-many)
            arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y), 
                                   connectionstyle='arc3,rad=0.1', 
                                   arrowstyle='->', 
                                   mutation_scale=15, 
                                   lw=1, 
                                   color=arrow_color)
        elif rel['type'] == 'O2O':
            # Double-headed arrow for OneToOneField (one-to-one)
            arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y), 
                                   connectionstyle='arc3,rad=0.1', 
                                   arrowstyle='<->', 
                                   mutation_scale=15, 
                                   lw=1, 
                                   color=arrow_color)
        elif rel['type'] == 'M2M':
            # Double-headed arrow with bars for ManyToManyField (many-to-many)
            arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y), 
                                   connectionstyle='arc3,rad=0.1', 
                                   arrowstyle='<|-|>', 
                                   mutation_scale=15, 
                                   lw=1, 
                                   color=arrow_color)
        
        ax.add_patch(arrow)

# Add title
# Add an overall title for the diagram
plt.title('Quiz Application Entity Relationship Diagram', fontsize=16, pad=20)

# Ensure output directory exists
# Create the directory for saving the diagram if it doesn't exist
os.makedirs('docs/_static', exist_ok=True)

# Save figure
# Save the diagram as a PNG file
plt.savefig('docs/_static/updated_erd_diagram.png', dpi=300, bbox_inches='tight')
print("ERD diagram saved to docs/_static/updated_erd_diagram.png")

# If running interactively, show the plot
# Display the diagram if the script is run directly
if __name__ == '__main__':
    print("Displaying ERD diagram...")
    plt.show() 