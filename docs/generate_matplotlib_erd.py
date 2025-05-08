"""
Generate a simplified Entity Relationship Diagram for the Quiz Game application.

This script uses matplotlib to create a visual representation
of the database schema, focusing on the relationships between models.

What does this script do?
-------------------------
This script creates a visual diagram showing how different parts of our quiz application
are connected. It's like drawing a map of our database that makes it easy to understand:
- What types of data we store (Users, Questions, Quizzes, etc.)
- How these data types relate to each other (Users can take Quizzes, etc.)
- Which relationships are regular vs. "virtual" (like Analytics)

The diagram uses colored boxes for different data types and arrows to show relationships.

Usage:
    python docs/generate_matplotlib_erd.py
"""

import os
import sys
import django
import matplotlib.pyplot as plt  # For creating the visualization
import matplotlib.patches as patches  # For drawing shapes
import numpy as np  # For numerical operations
from matplotlib.lines import Line2D  # For creating legend elements

# Add the parent directory to the Python path so we can import the project files
# This is technical setup to make sure Python can find our application code
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")
django.setup()

# Import all the models we want to include in our diagram
# These are the main data types in our application
from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse, UserProfile
from django.contrib.auth.models import User


def create_erd():
    """
    Create the Entity Relationship Diagram using matplotlib.
    
    This function:
    1. Sets up the diagram canvas
    2. Places each model as a colored box
    3. Draws arrows between related models
    4. Adds labels and a legend
    5. Saves the diagram as an image file
    
    No technical knowledge is needed to understand the final diagram.
    """
    # Set up the figure (canvas) where we'll draw our diagram
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Define where each model box will be positioned (x, y coordinates)
    # The values are between 0 and 1, representing percentage of the canvas
    positions = {
        'User': (0.2, 0.8),              # User box in top-left
        'UserProfile': (0.2, 0.2),       # UserProfile below User
        'Category': (0.5, 0.5),          # Category in the middle
        'Question': (0.8, 0.8),          # Question in top-right
        'Choice': (0.8, 0.2),            # Choice in bottom-right
        'QuizAttempt': (0.5, 0.2),       # QuizAttempt in bottom-middle
        'QuizResponse': (0.5, 0.8),      # QuizResponse in top-middle
        'Analytics': (0.8, 0.5)          # Analytics in middle-right
    }
    
    # Define a different color for each model box to make it visually distinct
    # Colors are in hex format (web colors)
    colors = {
        'User': '#B3E5FC',               # Light blue
        'UserProfile': '#C8E6C9',        # Light green
        'Category': '#FFE0B2',           # Light orange
        'Question': '#F8BBD0',           # Light pink
        'Choice': '#D1C4E9',             # Light purple
        'QuizAttempt': '#FFCCBC',        # Light deep orange
        'QuizResponse': '#CFD8DC',       # Light blue gray
        'Analytics': '#FFEB3B'           # Light yellow
    }
    
    # Draw each model as a colored box with its name
    boxes = {}
    for model_name, pos in positions.items():
        # Create a rounded rectangle for the model
        box = patches.FancyBboxPatch(
            (pos[0] - 0.1, pos[1] - 0.07),  # bottom-left corner
            0.2, 0.14,                       # width, height
            boxstyle=patches.BoxStyle("Round", pad=0.02),  # rounded corners
            facecolor=colors[model_name],    # fill color from our color dictionary
            edgecolor='black',               # border color
            linewidth=1                      # border thickness
        )
        ax.add_patch(box)
        
        # Add the model name as text inside the box
        ax.text(pos[0], pos[1], model_name, 
                ha='center', va='center',    # center the text
                fontsize=10, fontweight='bold')  # make it bold
        
        # Store the box position for drawing arrows later
        boxes[model_name] = pos
    
    # Define the relationships between models
    # Each relationship is defined as (source model, target model, relationship type)
    # The relationship type describes the cardinality (e.g., 1:n means "one-to-many")
    relationships = [
        # User relationships
        ('User', 'UserProfile', '1:1'),      # One user has one profile
        ('User', 'QuizAttempt', '1:n'),      # One user can take many quizzes
        
        # Category relationships
        ('Category', 'Question', '1:n'),     # One category has many questions
        ('Category', 'QuizAttempt', '1:n'),  # One category has many quiz attempts
        ('Category', 'UserProfile', '1:n'),  # Category can be favorite for many users
        
        # Question relationships
        ('Question', 'Choice', '1:n'),       # One question has many answer choices
        ('Question', 'QuizResponse', '1:n'), # One question has many responses
        
        # QuizAttempt relationships
        ('QuizAttempt', 'QuizResponse', '1:n'),  # One quiz attempt has many responses
        
        # Choice relationships
        ('Choice', 'QuizResponse', '1:n'),   # One choice can be selected in many responses
    ]
    
    # Draw arrows for each relationship
    for source, target, rel_type in relationships:
        # Get the positions of the source and target boxes
        start_x, start_y = boxes[source]
        end_x, end_y = boxes[target]
        
        # Calculate the middle point between source and target for the arrow curve
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Adjust the control point for the curve based on the alignment
        # This prevents arrow overlaps when boxes are aligned vertically or horizontally
        if abs(start_x - end_x) < 0.1:  # Vertical alignment
            control_x = mid_x + 0.15    # Offset the curve to the right
            control_y = mid_y
        elif abs(start_y - end_y) < 0.1:  # Horizontal alignment
            control_x = mid_x
            control_y = mid_y + 0.15    # Offset the curve upward
        else:
            control_x = mid_x
            control_y = mid_y
        
        # Create the arrow connection between the boxes
        arrow_path = patches.ConnectionPatch(
            (start_x, start_y), (end_x, end_y),
            "data", "data",               # Coordinate systems
            arrowstyle="-|>",             # Arrow style with a head
            connectionstyle=f"arc3,rad=0.1",  # Curved line
            shrinkA=10, shrinkB=10,       # Shorten the arrow to not touch the boxes
            linewidth=1                   # Line thickness
        )
        ax.add_patch(arrow_path)
        
        # Add a label for the relationship type (1:1, 1:n, etc.)
        text_x = control_x
        text_y = control_y
        plt.text(text_x, text_y, rel_type, 
                 fontsize=8, ha='center', va='center',  # Small centered text
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none',  # White background
                          boxstyle='round,pad=0.1'))    # Rounded box around text
    
    # Add special relationships for Analytics (which isn't a real model but a feature)
    # These are shown with dashed lines to indicate they're "virtual" relationships
    analytics_relationships = [
        ('QuizAttempt', 'Analytics', 'data'),    # Analytics processes quiz data
        ('QuizResponse', 'Analytics', 'data'),   # Analytics processes response data
        ('User', 'Analytics', 'view')            # Users view their analytics
    ]
    
    # Draw dashed arrows for the Analytics relationships
    for source, target, rel_type in analytics_relationships:
        start_x, start_y = boxes[source]
        end_x, end_y = boxes[target]
        
        # Calculate the midpoint for the curve
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2
        
        # Create a dashed arrow (showing a virtual/non-database relationship)
        arrow_path = patches.ConnectionPatch(
            (start_x, start_y), (end_x, end_y),
            "data", "data",
            arrowstyle="-|>",
            connectionstyle=f"arc3,rad=0.1",
            shrinkA=10, shrinkB=10,
            linewidth=1, 
            linestyle='dashed'            # Dashed line for virtual relationships
        )
        ax.add_patch(arrow_path)
        
        # Add a label for the relationship type
        control_x = mid_x + 0.05
        control_y = mid_y + 0.05
        plt.text(control_x, control_y, rel_type, 
                 fontsize=8, ha='center', va='center', 
                 bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', 
                           boxstyle='round,pad=0.1'))
    
    # Add a legend explaining what solid vs. dashed lines mean
    legend_elements = [
        Line2D([0], [0], color='black', lw=1, 
               label='Standard Relationship (stored in database)'),
        Line2D([0], [0], color='black', lw=1, linestyle='dashed', 
               label='Virtual Relationship (calculated on request)')
    ]
    ax.legend(handles=legend_elements, loc='upper center', bbox_to_anchor=(0.5, 0.05))
    
    # Remove the axis to make it look cleaner
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    # Add a title to the diagram
    plt.title('Quiz Game Entity Relationship Diagram with Analytics', fontsize=14, pad=20)
    
    # Create the _static directory if it doesn't exist
    os.makedirs('docs/_static', exist_ok=True)
    
    # Save the diagram as a PNG image
    plt.tight_layout()
    plt.savefig('docs/_static/erd_diagram_matplotlib.png', dpi=300, bbox_inches='tight')
    print("ERD diagram has been generated at docs/_static/erd_diagram_matplotlib.png")
    
    # Close the plot to free memory
    plt.close()


if __name__ == "__main__":
    # Only run this code when the script is executed directly (not imported)
    create_erd() 