"""
Generate a simplified Entity Relationship Diagram for the Quiz Game application.

This script uses matplotlib to create a visual representation
of the database schema, focusing on the relationships between models.

Usage:
    python docs/generate_matplotlib_erd.py
"""

import os
import sys
import django
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Add the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")
django.setup()

# Import the models
from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse, UserProfile
from django.contrib.auth.models import User


def create_erd():
    """Create the ERD diagram using matplotlib."""
    # Set up figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define model positions (x, y)
    positions = {
        'User': (0.2, 0.8),
        'UserProfile': (0.2, 0.2),
        'Category': (0.5, 0.5),
        'Question': (0.8, 0.8),
        'Choice': (0.8, 0.2),
        'QuizAttempt': (0.5, 0.2),
        'QuizResponse': (0.5, 0.8)
    }
    
    # Define model colors
    colors = {
        'User': '#B3E5FC',  # Light blue
        'UserProfile': '#C8E6C9',  # Light green
        'Category': '#FFE0B2',  # Light orange
        'Question': '#F8BBD0',  # Light pink
        'Choice': '#D1C4E9',  # Light purple
        'QuizAttempt': '#FFCCBC',  # Light deep orange
        'QuizResponse': '#CFD8DC'  # Light blue gray
    }
    
    # Draw model boxes
    boxes = {}
    for model_name, pos in positions.items():
        # Create a box for each model
        box = patches.FancyBboxPatch(
            (pos[0] - 0.1, pos[1] - 0.07),  # bottom-left corner
            0.2, 0.14,  # width, height
            boxstyle=patches.BoxStyle("Round", pad=0.02),
            facecolor=colors[model_name],
            edgecolor='black',
            linewidth=1
        )
        ax.add_patch(box)
        
        # Add model name text
        ax.text(pos[0], pos[1], model_name, ha='center', va='center', fontsize=10, fontweight='bold')
        
        # Store box reference for drawing arrows
        boxes[model_name] = pos
    
    # Define relationships
    relationships = [
        # (source, target, relationship_type)
        ('User', 'UserProfile', '1:1'),
        ('User', 'QuizAttempt', '1:n'),
        ('Category', 'Question', '1:n'),
        ('Category', 'QuizAttempt', '1:n'),
        ('Category', 'UserProfile', '1:n'),
        ('Question', 'Choice', '1:n'),
        ('Question', 'QuizResponse', '1:n'),
        ('QuizAttempt', 'QuizResponse', '1:n'),
        ('Choice', 'QuizResponse', '1:n')
    ]
    
    # Draw relationship arrows
    for source, target, rel_type in relationships:
        start_x, start_y = boxes[source]
        end_x, end_y = boxes[target]
        
        # Calculate control points for curved arrows
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Adjust control point for vertical/horizontal alignment
        if abs(start_x - end_x) < 0.1:  # Vertical alignment
            control_x = mid_x + 0.15
            control_y = mid_y
        elif abs(start_y - end_y) < 0.1:  # Horizontal alignment
            control_x = mid_x
            control_y = mid_y + 0.15
        else:
            control_x = mid_x
            control_y = mid_y
        
        # Create arrow path
        arrow_path = patches.ConnectionPatch(
            (start_x, start_y), (end_x, end_y),
            "data", "data",
            arrowstyle="-|>",
            connectionstyle=f"arc3,rad=0.1",
            shrinkA=10, shrinkB=10,
            linewidth=1
        )
        ax.add_patch(arrow_path)
        
        # Add relationship type text
        text_x = control_x
        text_y = control_y
        plt.text(text_x, text_y, rel_type, fontsize=8, ha='center', va='center', 
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', boxstyle='round,pad=0.1'))
    
    # Set plot limits and remove axes
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Set title
    plt.title('Quiz Game Entity Relationship Diagram', fontsize=14, pad=20)
    
    # Save the diagram
    os.makedirs('docs/_static', exist_ok=True)
    plt.tight_layout()
    plt.savefig('docs/_static/erd_diagram_matplotlib.png', dpi=300, bbox_inches='tight')
    print("ERD diagram has been generated at docs/_static/erd_diagram_matplotlib.png")
    
    # Close the plot
    plt.close()


if __name__ == "__main__":
    create_erd() 