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
BORDER_COLOR = '#2C3E50'  # Dark blue-gray for borders
BACKGROUND_COLOR = '#FFFFFF'  # Pure white background

def draw_actor(ax, x, y, name):
    """Draw an actor with a stick figure and label."""
    # Draw subtle shadow
    shadow_offset = 0.03
    head_shadow = plt.Circle((x + shadow_offset, y+0.7 - shadow_offset), 0.2, 
                          fill=True, color='#DDDDDD', alpha=0.5)
    ax.add_patch(head_shadow)
    
    # Draw the head with improved styling
    head = plt.Circle((x, y+0.7), 0.2, fill=True, 
                    facecolor=ACTOR_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5)
    ax.add_patch(head)
    
    # Draw the body with thicker line
    ax.plot([x, x], [y+0.5, y-0.1], color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
    
    # Draw the arms with thicker line and rounded caps
    ax.plot([x-0.3, x+0.3], [y+0.3, y+0.3], color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
    
    # Draw the legs with thicker line and rounded caps
    ax.plot([x, x-0.3], [y-0.1, y-0.5], color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
    ax.plot([x, x+0.3], [y-0.1, y-0.5], color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
    
    # Add label with better styling
    label_box = patches.FancyBboxPatch(
        (x-0.6, y-1.1), 1.2, 0.4,
        boxstyle=patches.BoxStyle("Round", pad=0.2),
        facecolor=ACTOR_COLOR, edgecolor=BORDER_COLOR, linewidth=1, alpha=0.9
    )
    ax.add_patch(label_box)
    ax.text(x, y-0.9, name, ha='center', va='center', fontsize=9, fontweight='bold')

def draw_usecase(ax, x, y, width, height, name):
    """Draw a use case (ellipse) with text."""
    # Add subtle shadow for depth
    shadow = patches.Ellipse((x + 0.03, y - 0.03), width, height, fill=True, 
                            facecolor='#DDDDDD', edgecolor='none', alpha=0.5)
    ax.add_patch(shadow)
    
    # Draw main ellipse with improved styling
    ellipse = patches.Ellipse((x, y), width, height, fill=True, 
                             facecolor=USECASE_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5)
    ax.add_patch(ellipse)
    
    # Add label with improved styling
    ax.text(x, y, name, ha='center', va='center', fontsize=9, fontweight='bold')

def draw_system_boundary(ax, x, y, width, height, name):
    """Draw a system boundary rectangle with title."""
    # Draw subtle shadow
    shadow = patches.Rectangle((x + 0.05, y - 0.05), width, height, fill=True, 
                             facecolor='#DDDDDD', edgecolor='none', alpha=0.3)
    ax.add_patch(shadow)
    
    # Draw rectangle with improved styling
    rect = patches.Rectangle((x, y), width, height, fill=True, 
                            facecolor=SYSTEM_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5,
                            alpha=0.5, linestyle='dashed')
    ax.add_patch(rect)
    
    # Draw title area with improved styling
    title_box = patches.FancyBboxPatch(
        (x, y+height-0.7), width, 0.7, 
        boxstyle=patches.BoxStyle("Round", pad=0.2),
        facecolor=SYSTEM_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5,
        alpha=0.9
    )
    ax.add_patch(title_box)
    
    # Add label with improved styling
    ax.text(x+width/2, y+height-0.35, name, ha='center', va='center', 
            fontsize=12, fontweight='bold', color=BORDER_COLOR)

def draw_association(ax, start, end):
    """Draw an association line between actor and use case."""
    # Calculate a slight curve for more elegant appearance
    # Create the curve points
    t = np.linspace(0, 1, 30)
    # Set a very small offset for a subtle curve
    curve_offset = min(0.1, np.sqrt((end[0]-start[0])**2 + (end[1]-start[1])**2) * 0.05)
    
    # Determine direction of curve
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # Adjust control point based on direction
    if abs(dx) > abs(dy):
        # Horizontal flow - subtle vertical offset
        control = (start[0] + dx/2, start[1] + dy/2 + curve_offset)
    else:
        # Vertical flow - subtle horizontal offset
        control = (start[0] + dx/2 + curve_offset, start[1] + dy/2)
    
    # Quadratic Bezier curve
    curve_x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
    curve_y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
    
    # Draw the curve with smoother line
    ax.plot(curve_x, curve_y, color=ARROW_COLOR, linewidth=1.5, solid_capstyle='round')

def draw_include(ax, start, end, label_offset=(0,0)):
    """Draw an include relationship between use cases."""
    # Calculate control point for smoother curve
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = np.sqrt(dx**2 + dy**2)
    curve_factor = min(0.2, distance * 0.1)
    
    # Draw dashed arrow with curve
    t = np.linspace(0, 1, 30)
    control = (start[0] + dx/2 + dy*curve_factor, start[1] + dy/2 - dx*curve_factor)
    
    # Create the Bezier curve
    curve_x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
    curve_y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
    
    # Draw the curve
    ax.plot(curve_x, curve_y, color=INCLUDE_COLOR, linewidth=1.5, 
           linestyle='dashed', dashes=(5, 3), solid_capstyle='round')
    
    # Add arrowhead
    arrow_length = 0.15
    arrow_width = 0.08
    
    # Calculate the direction at the end point
    end_direction = np.array([curve_x[-1] - curve_x[-2], curve_y[-1] - curve_y[-2]])
    end_direction = end_direction / np.linalg.norm(end_direction)
    normal = np.array([-end_direction[1], end_direction[0]])
    
    # Calculate arrowhead points
    arrow_tip = np.array(end)
    arrow_base = arrow_tip - arrow_length * end_direction
    arrow_left = arrow_base + arrow_width * normal
    arrow_right = arrow_base - arrow_width * normal
    
    # Draw arrowhead
    arrow = patches.Polygon(
        [arrow_tip, arrow_left, arrow_right],
        facecolor=INCLUDE_COLOR,
        edgecolor='none'
    )
    ax.add_patch(arrow)
    
    # Add label with enhanced styling
    midpoint = ((start[0] + end[0])/2 + label_offset[0], 
                (start[1] + end[1])/2 + label_offset[1])
    ax.text(midpoint[0], midpoint[1], "<<include>>", 
            ha='center', va='center', fontsize=8, color=INCLUDE_COLOR,
            bbox=dict(facecolor='white', alpha=0.95, boxstyle='round,pad=0.2', 
                     edgecolor=INCLUDE_COLOR, linestyle='dotted', linewidth=1))

def draw_extend(ax, start, end, label_offset=(0,0)):
    """Draw an extend relationship between use cases."""
    # Calculate control point for smoother curve
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = np.sqrt(dx**2 + dy**2)
    curve_factor = min(0.2, distance * 0.1)
    
    # Draw dashed arrow with curve
    t = np.linspace(0, 1, 30)
    control = (start[0] + dx/2 - dy*curve_factor, start[1] + dy/2 + dx*curve_factor)
    
    # Create the Bezier curve
    curve_x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
    curve_y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
    
    # Draw the curve
    ax.plot(curve_x, curve_y, color=EXTEND_COLOR, linewidth=1.5, 
           linestyle='dashed', dashes=(5, 3), solid_capstyle='round')
    
    # Add arrowhead
    arrow_length = 0.15
    arrow_width = 0.08
    
    # Calculate the direction at the end point
    end_direction = np.array([curve_x[-1] - curve_x[-2], curve_y[-1] - curve_y[-2]])
    end_direction = end_direction / np.linalg.norm(end_direction)
    normal = np.array([-end_direction[1], end_direction[0]])
    
    # Calculate arrowhead points
    arrow_tip = np.array(end)
    arrow_base = arrow_tip - arrow_length * end_direction
    arrow_left = arrow_base + arrow_width * normal
    arrow_right = arrow_base - arrow_width * normal
    
    # Draw arrowhead
    arrow = patches.Polygon(
        [arrow_tip, arrow_left, arrow_right],
        facecolor=EXTEND_COLOR,
        edgecolor='none'
    )
    ax.add_patch(arrow)
    
    # Add label with enhanced styling
    midpoint = ((start[0] + end[0])/2 + label_offset[0], 
                (start[1] + end[1])/2 + label_offset[1])
    ax.text(midpoint[0], midpoint[1], "<<extend>>", 
            ha='center', va='center', fontsize=8, color=EXTEND_COLOR,
            bbox=dict(facecolor='white', alpha=0.95, boxstyle='round,pad=0.2', 
                     edgecolor=EXTEND_COLOR, linestyle='dotted', linewidth=1))

def generate_use_case_diagram():
    """Generate a use case diagram for the Quiz Application."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw subtle grid for better alignment (won't be visible in output)
    ax.grid(True, linestyle='--', alpha=0.1)
    
    # Draw system boundary
    draw_system_boundary(ax, 2.5, 1, 7, 8, "Quiz System")
    
    # Draw actors
    draw_actor(ax, 1, 8, "Anonymous\nUser")
    draw_actor(ax, 1, 5, "Registered\nUser")
    draw_actor(ax, 1, 2, "Administrator")
    
    # Draw use cases with improved spacing
    # Anonymous user use cases
    draw_usecase(ax, 4.2, 8, 2.2, 0.9, "View Available Quizzes")
    draw_usecase(ax, 4.2, 7, 2.2, 0.9, "Register Account")
    draw_usecase(ax, 6.2, 7, 2.2, 0.9, "Login")
    
    # Registered user use cases
    draw_usecase(ax, 4.2, 6, 2.2, 0.9, "Select Quiz Category")
    draw_usecase(ax, 4.2, 5, 2.2, 0.9, "Take Quiz")
    draw_usecase(ax, 4.2, 4, 2.2, 0.9, "View Results")
    draw_usecase(ax, 6.2, 5, 2.2, 0.9, "View Personal Stats")
    draw_usecase(ax, 6.2, 4, 2.2, 0.9, "Update Profile")
    
    # Administrator use cases
    draw_usecase(ax, 6.2, 2.5, 2.2, 0.9, "Manage Questions")
    draw_usecase(ax, 6.2, 1.5, 2.2, 0.9, "Manage Categories")
    draw_usecase(ax, 4.2, 2, 2.2, 0.9, "View System Stats")
    
    # Extended/Included use cases
    draw_usecase(ax, 8.2, 6, 2.2, 0.9, "Set Quiz Options")
    draw_usecase(ax, 8.2, 3, 2.2, 0.9, "Generate Reports")
    
    # Draw associations with improved positioning
    # Anonymous user associations
    draw_association(ax, (1.3, 8), (3.1, 8))
    draw_association(ax, (1.2, 7.8), (3.1, 7))
    draw_association(ax, (1.3, 7.6), (5.1, 7))
    
    # Registered user associations
    draw_association(ax, (1.3, 5), (3.1, 6))
    draw_association(ax, (1.3, 5), (3.1, 5))
    draw_association(ax, (1.3, 5), (3.1, 4))
    draw_association(ax, (1.3, 5), (5.1, 5))
    draw_association(ax, (1.3, 5), (5.1, 4))
    
    # Administrator associations
    draw_association(ax, (1.3, 2), (5.1, 2.5))
    draw_association(ax, (1.3, 2), (5.1, 1.5))
    draw_association(ax, (1.3, 2), (3.1, 2))
    
    # Draw include relationships with improved positioning
    draw_include(ax, (5.3, 5), (7.1, 6), (0, 0.2))
    draw_include(ax, (5.3, 2), (7.1, 3), (0, 0.2))
    
    # Draw extend relationships with improved positioning
    draw_extend(ax, (5.5, 4), (5, 4.5), (0.2, 0))
    draw_extend(ax, (7.2, 2.5), (7.2, 3), (0.3, 0))
    
    # Add title with enhanced styling
    ax.set_title("Quiz System Use Case Diagram", 
                 fontsize=16, pad=20, fontweight='bold', 
                 bbox=dict(facecolor='white', edgecolor='#E0E0E0', boxstyle='round,pad=0.5'))
    
    # Add subtle watermark
    fig.text(0.95, 0.05, "Quiz App", fontsize=12, color='lightgray', 
             ha='right', va='bottom', alpha=0.3, fontweight='bold')
    
    # Save the figure with higher quality
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/use_case_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Use case diagram has been generated in docs/diagrams/output/use_case_diagram.png")

if __name__ == "__main__":
    generate_use_case_diagram() 