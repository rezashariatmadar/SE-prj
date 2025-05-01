#!/usr/bin/env python
"""
Generate Use Case Diagram for the Quiz application.

This script creates a UML use case diagram for the Quiz Application using matplotlib.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.path import Path
import numpy as np

# Create output directory if it doesn't exist
os.makedirs('docs/diagrams/output', exist_ok=True)

# Define colors
ACTOR_COLOR = '#FFD580'  # Light orange
USECASE_COLOR = '#B3E5FC'  # Light blue
SYSTEM_COLOR = '#F5F5F5'  # Very light gray
ARROW_COLOR = '#616161'  # Dark gray
INCLUDE_COLOR = '#4CAF50'  # Green
EXTEND_COLOR = '#F44336'  # Red

def draw_actor(ax, x, y, name):
    """Draw an actor with a stick figure and label."""
    # Draw the head
    head = plt.Circle((x, y+0.7), 0.2, fill=True, color=ACTOR_COLOR, edgecolor='black', linewidth=1)
    ax.add_patch(head)
    
    # Draw the body
    ax.plot([x, x], [y+0.5, y-0.1], color='black', linewidth=2)
    
    # Draw the arms
    ax.plot([x-0.3, x+0.3], [y+0.3, y+0.3], color='black', linewidth=2)
    
    # Draw the legs
    ax.plot([x, x-0.3], [y-0.1, y-0.5], color='black', linewidth=2)
    ax.plot([x, x+0.3], [y-0.1, y-0.5], color='black', linewidth=2)
    
    # Add label
    ax.text(x, y-0.7, name, ha='center', va='top', fontsize=10, fontweight='bold')

def draw_usecase(ax, x, y, width, height, name):
    """Draw a use case (ellipse) with text."""
    ellipse = patches.Ellipse((x, y), width, height, fill=True, 
                             facecolor=USECASE_COLOR, edgecolor='black', linewidth=1)
    ax.add_patch(ellipse)
    
    # Add label
    ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold')

def draw_system_boundary(ax, x, y, width, height, name):
    """Draw a system boundary rectangle with title."""
    # Draw rectangle
    rect = patches.Rectangle((x, y), width, height, fill=True, 
                            facecolor=SYSTEM_COLOR, edgecolor='black', linewidth=1,
                            alpha=0.5)
    ax.add_patch(rect)
    
    # Draw title area
    title_box = patches.Rectangle((x, y+height-0.7), width, 0.7, fill=True, 
                                 facecolor=SYSTEM_COLOR, edgecolor='black', linewidth=1,
                                 alpha=0.8)
    ax.add_patch(title_box)
    
    # Add label
    ax.text(x+width/2, y+height-0.35, name, ha='center', va='center', 
            fontsize=12, fontweight='bold')

def draw_association(ax, start, end):
    """Draw an association line between actor and use case."""
    ax.plot([start[0], end[0]], [start[1], end[1]], color=ARROW_COLOR, 
            linewidth=1.5, linestyle='-')

def draw_include(ax, start, end, label_offset=(0,0)):
    """Draw an include relationship between use cases."""
    # Draw dashed arrow
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="->", color=INCLUDE_COLOR, 
                             lw=1.5, connectionstyle="arc3,rad=0.1",
                             linestyle='dashed'))
    
    # Add label
    midpoint = ((start[0] + end[0])/2 + label_offset[0], 
                (start[1] + end[1])/2 + label_offset[1])
    ax.text(midpoint[0], midpoint[1], "<<include>>", 
            ha='center', va='center', fontsize=8, color=INCLUDE_COLOR,
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.2', edgecolor='none'))

def draw_extend(ax, start, end, label_offset=(0,0)):
    """Draw an extend relationship between use cases."""
    # Draw dashed arrow
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="->", color=EXTEND_COLOR, 
                             lw=1.5, connectionstyle="arc3,rad=0.1",
                             linestyle='dashed'))
    
    # Add label
    midpoint = ((start[0] + end[0])/2 + label_offset[0], 
                (start[1] + end[1])/2 + label_offset[1])
    ax.text(midpoint[0], midpoint[1], "<<extend>>", 
            ha='center', va='center', fontsize=8, color=EXTEND_COLOR,
            bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.2', edgecolor='none'))

def generate_use_case_diagram():
    """Generate a use case diagram for the Quiz Application."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    # Draw system boundary
    draw_system_boundary(ax, 2.5, 1, 7, 8, "Quiz System")
    
    # Draw actors
    draw_actor(ax, 1, 8, "Anonymous\nUser")
    draw_actor(ax, 1, 5, "Registered\nUser")
    draw_actor(ax, 1, 2, "Administrator")
    
    # Draw use cases
    # Anonymous user use cases
    draw_usecase(ax, 4, 8, 2, 0.8, "View Available Quizzes")
    draw_usecase(ax, 4, 7, 2, 0.8, "Register Account")
    draw_usecase(ax, 6, 7, 2, 0.8, "Login")
    
    # Registered user use cases
    draw_usecase(ax, 4, 6, 2, 0.8, "Select Quiz Category")
    draw_usecase(ax, 4, 5, 2, 0.8, "Take Quiz")
    draw_usecase(ax, 4, 4, 2, 0.8, "View Results")
    draw_usecase(ax, 6, 5, 2, 0.8, "View Personal Stats")
    draw_usecase(ax, 6, 4, 2, 0.8, "Update Profile")
    
    # Administrator use cases
    draw_usecase(ax, 6, 2.5, 2, 0.8, "Manage Questions")
    draw_usecase(ax, 6, 1.5, 2, 0.8, "Manage Categories")
    draw_usecase(ax, 4, 2, 2, 0.8, "View System Stats")
    
    # Extended/Included use cases
    draw_usecase(ax, 8, 6, 2, 0.8, "Set Quiz Options")
    draw_usecase(ax, 8, 3, 2, 0.8, "Generate Reports")
    
    # Draw associations
    # Anonymous user associations
    draw_association(ax, (1.3, 8), (3, 8))
    draw_association(ax, (1.2, 7.8), (3, 7))
    draw_association(ax, (1.3, 7.6), (5, 7))
    
    # Registered user associations
    draw_association(ax, (1.3, 5), (3, 6))
    draw_association(ax, (1.3, 5), (3, 5))
    draw_association(ax, (1.3, 5), (3, 4))
    draw_association(ax, (1.3, 5), (5, 5))
    draw_association(ax, (1.3, 5), (5, 4))
    
    # Administrator associations
    draw_association(ax, (1.3, 2), (5, 2.5))
    draw_association(ax, (1.3, 2), (5, 1.5))
    draw_association(ax, (1.3, 2), (3, 2))
    
    # Draw include relationships
    draw_include(ax, (5, 5), (7, 6), (0, 0.2))
    draw_include(ax, (5.5, 2), (7, 3), (0, 0.2))
    
    # Draw extend relationships
    draw_extend(ax, (5.5, 4), (5, 4.5), (0.2, 0))
    draw_extend(ax, (7, 2.5), (7, 3), (0.3, 0))
    
    # Add title
    ax.set_title("Quiz System Use Case Diagram", fontsize=14, pad=20)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/use_case_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Use case diagram has been generated in docs/diagrams/output/use_case_diagram.png")

if __name__ == "__main__":
    generate_use_case_diagram() 