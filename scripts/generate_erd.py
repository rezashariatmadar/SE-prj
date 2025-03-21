#!/usr/bin/env python
"""
Generate an Entity Relationship Diagram for the Quiz application models using matplotlib.
"""

import os
import sys
import django
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle, FancyArrowPatch

# Set up Django environment
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'quiz_project.settings')
django.setup()

from django.apps import apps
from django.db.models.fields.related import ForeignKey, OneToOneField, ManyToManyField

# Get all models from the quiz_app
app_models = apps.get_app_config('quiz_app').get_models()

# Create a figure
fig, ax = plt.subplots(figsize=(16, 12))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)

# Hide axes
ax.axis('off')

# Define colors
model_color = '#E5F5E0'
border_color = '#31a354'
header_color = '#A1D99B'
title_color = '#006D2C'
arrow_color = '#636363'

# Calculate positions based on number of models
model_width = 18
model_height = 0  # Will be calculated based on fields
model_padding = 5
models_per_row = 3
horizontal_spacing = (100 - (models_per_row * model_width)) / (models_per_row + 1)

# Dictionaries to store model positions
model_positions = {}
relation_arrows = []

# Arrange models in a grid
row = 0
col = 0
max_height_in_row = 0
vertical_position = 90  # Start from top

for i, model in enumerate(sorted(app_models, key=lambda m: m.__name__)):
    # Calculate height based on number of fields
    fields = model._meta.get_fields()
    field_height = 1.5
    header_height = 3
    model_height = header_height + (len(fields) * field_height)
    
    # Adjust position if we need a new row
    if col >= models_per_row:
        col = 0
        row += 1
        vertical_position -= max_height_in_row + model_padding
        max_height_in_row = 0
    
    # Calculate position
    x = horizontal_spacing + col * (model_width + horizontal_spacing)
    y = vertical_position - model_height
    
    # Store position for relationships
    model_positions[model] = {
        'x': x, 
        'y': y, 
        'width': model_width, 
        'height': model_height,
        'fields': {f.name: i for i, f in enumerate(fields)}
    }
    
    # Update max height in row
    max_height_in_row = max(max_height_in_row, model_height)
    
    # Draw model box
    rect = Rectangle((x, y), model_width, model_height, 
                    facecolor=model_color, edgecolor=border_color, lw=1)
    ax.add_patch(rect)
    
    # Draw header
    header_rect = Rectangle((x, y + model_height - header_height), model_width, header_height, 
                           facecolor=header_color, edgecolor=border_color, lw=1)
    ax.add_patch(header_rect)
    
    # Add model name
    ax.text(x + model_width/2, y + model_height - header_height/2, model.__name__, 
            ha='center', va='center', fontsize=12, fontweight='bold', color=title_color)
    
    # Add fields
    for j, field in enumerate(fields):
        field_y = y + model_height - header_height - (j + 1) * field_height + field_height/2
        field_text = field.name
        
        # Identify field type for relationships
        if isinstance(field, ForeignKey):
            field_text += f' → {field.related_model.__name__}'
            relation_arrows.append({
                'from_model': model,
                'from_field': field.name,
                'to_model': field.related_model,
                'type': 'FK'
            })
        elif isinstance(field, OneToOneField):
            field_text += f' ↔ {field.related_model.__name__}'
            relation_arrows.append({
                'from_model': model,
                'from_field': field.name,
                'to_model': field.related_model,
                'type': 'O2O'
            })
        elif isinstance(field, ManyToManyField):
            field_text += f' ⇆ {field.related_model.__name__}'
            relation_arrows.append({
                'from_model': model,
                'from_field': field.name,
                'to_model': field.related_model,
                'type': 'M2M'
            })
            
        ax.text(x + 0.5, field_y, field_text, fontsize=10, va='center')
    
    # Increment column
    col += 1

# Draw relationship arrows
for rel in relation_arrows:
    if rel['to_model'] in model_positions and rel['from_model'] in model_positions:
        from_pos = model_positions[rel['from_model']]
        to_pos = model_positions[rel['to_model']]
        
        # Calculate arrow positions
        from_field_idx = from_pos['fields'].get(rel['from_field'], 0)
        from_y = from_pos['y'] + from_pos['height'] - 3 - (from_field_idx + 1) * 1.5 + 1.5/2
        
        # Start and end positions
        start_x = from_pos['x'] + from_pos['width']
        start_y = from_y
        end_x = to_pos['x']
        end_y = to_pos['y'] + to_pos['height'] - 1.5  # Point to top of model
        
        # Draw arrow based on relationship type
        if rel['type'] == 'FK':
            arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y), 
                                   connectionstyle='arc3,rad=0.1', 
                                   arrowstyle='->', 
                                   mutation_scale=15, 
                                   lw=1, 
                                   color=arrow_color)
        elif rel['type'] == 'O2O':
            arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y), 
                                   connectionstyle='arc3,rad=0.1', 
                                   arrowstyle='<->', 
                                   mutation_scale=15, 
                                   lw=1, 
                                   color=arrow_color)
        elif rel['type'] == 'M2M':
            arrow = FancyArrowPatch((start_x, start_y), (end_x, end_y), 
                                   connectionstyle='arc3,rad=0.1', 
                                   arrowstyle='<|-|>', 
                                   mutation_scale=15, 
                                   lw=1, 
                                   color=arrow_color)
        
        ax.add_patch(arrow)

# Add title
plt.title('Quiz Application Entity Relationship Diagram', fontsize=16, pad=20)

# Ensure output directory exists
os.makedirs('docs/_static', exist_ok=True)

# Save figure
plt.savefig('docs/_static/updated_erd_diagram.png', dpi=300, bbox_inches='tight')
print("ERD diagram saved to docs/_static/updated_erd_diagram.png")

# If running interactively, show the plot
if __name__ == '__main__':
    print("Displaying ERD diagram...")
    plt.show() 