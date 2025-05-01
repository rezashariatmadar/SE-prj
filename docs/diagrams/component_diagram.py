#!/usr/bin/env python
"""
Generate Component Diagram for the Quiz application.

This script creates a UML component diagram showing the architecture
of the Quiz Application using matplotlib.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path

# Create output directory if it doesn't exist
os.makedirs('docs/diagrams/output', exist_ok=True)

# Define colors
COMPONENT_COLOR = '#BBDEFB'  # Light blue
INTERFACE_COLOR = '#FFECB3'  # Light amber
DATABASE_COLOR = '#E1BEE7'  # Light purple
DEPENDENCY_COLOR = '#616161'  # Dark gray
BACKGROUND_COLOR = '#FAFAFA'  # Off-white
BORDER_COLOR = 'black'

def draw_component(ax, x, y, width, height, name):
    """Draw a component box with the UML component symbol."""
    # Draw main rectangle
    rect = patches.Rectangle((x, y), width, height, fill=True,
                            facecolor=COMPONENT_COLOR, edgecolor=BORDER_COLOR, linewidth=1)
    ax.add_patch(rect)
    
    # Draw component symbol (small rectangles on the left side)
    symbol_x = x + 0.15
    symbol_y = y + height - 0.3
    symbol_width = 0.3
    symbol_height = 0.15
    
    # Upper rectangle
    rect1 = patches.Rectangle((symbol_x, symbol_y), symbol_width, symbol_height, fill=True,
                             facecolor=COMPONENT_COLOR, edgecolor=BORDER_COLOR, linewidth=1)
    ax.add_patch(rect1)
    
    # Lower rectangle
    rect2 = patches.Rectangle((symbol_x, symbol_y-0.2), symbol_width, symbol_height, fill=True,
                             facecolor=COMPONENT_COLOR, edgecolor=BORDER_COLOR, linewidth=1)
    ax.add_patch(rect2)
    
    # Add component name
    ax.text(x + width/2, y + height/2, name, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Return center positions for connection points
    return {
        'top': (x + width/2, y + height),
        'right': (x + width, y + height/2),
        'bottom': (x + width/2, y),
        'left': (x, y + height/2),
        'center': (x + width/2, y + height/2)
    }

def draw_interface(ax, x, y, radius, name, provided=True):
    """Draw an interface lollipop or socket."""
    if provided:
        # Provided interface (lollipop)
        circle = plt.Circle((x, y), radius, fill=False, edgecolor=BORDER_COLOR, linewidth=1.5)
        ax.add_patch(circle)
    else:
        # Required interface (socket)
        # Draw a semicircle
        theta = np.linspace(0, 180, 30) * np.pi / 180
        x_socket = x + radius * np.cos(theta)
        y_socket = y + radius * np.sin(theta)
        ax.plot(x_socket, y_socket, color=BORDER_COLOR, linewidth=1.5)
    
    # Add interface name
    offset = radius + 0.2
    if provided:
        ax.text(x, y - offset, name, ha='center', va='top', fontsize=8)
    else:
        ax.text(x, y - offset, name, ha='center', va='top', fontsize=8)
    
    return (x, y)

def draw_database(ax, x, y, width, height, name):
    """Draw a database cylinder."""
    # Draw the cylinder body
    rect = patches.Rectangle((x, y), width, height-0.5, fill=True,
                            facecolor=DATABASE_COLOR, edgecolor=BORDER_COLOR, linewidth=1)
    ax.add_patch(rect)
    
    # Draw the top ellipse
    ellipse_top = patches.Ellipse((x + width/2, y + height-0.5), width, 0.5, fill=True,
                                 facecolor=DATABASE_COLOR, edgecolor=BORDER_COLOR, linewidth=1)
    ax.add_patch(ellipse_top)
    
    # Draw the bottom ellipse
    ellipse_bottom = patches.Ellipse((x + width/2, y), width, 0.5, fill=True,
                                    facecolor=DATABASE_COLOR, edgecolor=BORDER_COLOR, linewidth=1)
    ax.add_patch(ellipse_bottom)
    
    # Add database name
    ax.text(x + width/2, y + height/2, name, ha='center', va='center', fontsize=10, fontweight='bold')
    
    return (x + width/2, y + height/2)

def draw_dependency(ax, start, end, label=None, style='solid'):
    """Draw a dependency arrow between components."""
    linestyle = '-' if style == 'solid' else '--'
    
    # Draw arrow
    ax.annotate('', xy=end, xytext=start,
               arrowprops=dict(arrowstyle='->', color=DEPENDENCY_COLOR, 
                            lw=1.5, connectionstyle='arc3,rad=0.1',
                            linestyle=linestyle))
    
    # Add label if provided
    if label:
        midpoint = ((start[0] + end[0])/2, (start[1] + end[1])/2)
        ax.text(midpoint[0], midpoint[1], label, ha='center', va='center', fontsize=8,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2', edgecolor='none'))

def generate_component_diagram():
    """Generate a component diagram for the Quiz Application."""
    fig, ax = plt.subplots(figsize=(12, 9))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 9)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw system boundary
    boundary = patches.Rectangle((0.5, 0.5), 11, 8, fill=False, 
                               edgecolor=BORDER_COLOR, linewidth=1.5, linestyle='--')
    ax.add_patch(boundary)
    ax.text(6, 8.7, "Quiz System", ha='center', va='center', fontsize=14, fontweight='bold')
    
    # Draw components
    # Front-end components
    ui_pos = draw_component(ax, 1, 6, 2, 1, "Browser UI")
    auth_pos = draw_component(ax, 1, 4, 2, 1, "Authentication")
    
    # Application layer components
    quiz_controller_pos = draw_component(ax, 4, 6, 2, 1, "Quiz Controller")
    user_controller_pos = draw_component(ax, 4, 4, 2, 1, "User Controller")
    admin_controller_pos = draw_component(ax, 4, 2, 2, 1, "Admin Controller")
    
    # Business logic components
    quiz_service_pos = draw_component(ax, 7, 6, 2, 1, "Quiz Service")
    stats_service_pos = draw_component(ax, 7, 4, 2, 1, "Statistics Service")
    user_service_pos = draw_component(ax, 7, 2, 2, 1, "User Service")
    
    # Data access components
    quiz_model_pos = draw_component(ax, 4, 0.5, 1.5, 1, "Quiz Model")
    user_model_pos = draw_component(ax, 6.5, 0.5, 1.5, 1, "User Model")
    
    # Databases
    quiz_db = draw_database(ax, 9.5, 5.5, 1.5, 1.5, "Quiz DB")
    user_db = draw_database(ax, 9.5, 1.5, 1.5, 1.5, "User DB")
    
    # Draw interfaces
    # Quiz Controller interfaces
    quiz_api = draw_interface(ax, quiz_controller_pos['right'][0], quiz_controller_pos['right'][1], 
                             0.15, "Quiz API", provided=True)
    
    # User Controller interfaces
    user_api = draw_interface(ax, user_controller_pos['right'][0], user_controller_pos['right'][1], 
                             0.15, "User API", provided=True)
    
    # Draw dependencies - Front-end to controllers
    draw_dependency(ax, ui_pos['right'], quiz_controller_pos['left'], "HTTP")
    draw_dependency(ax, ui_pos['bottom'], auth_pos['top'])
    draw_dependency(ax, auth_pos['right'], user_controller_pos['left'], "HTTP")
    
    # Draw dependencies - Controllers to Services
    draw_dependency(ax, quiz_controller_pos['right'], quiz_service_pos['left'])
    draw_dependency(ax, quiz_controller_pos['bottom'], stats_service_pos['left'], None, 'dashed')
    draw_dependency(ax, user_controller_pos['right'], user_service_pos['left'])
    draw_dependency(ax, admin_controller_pos['right'], quiz_service_pos['left'], None, 'dashed')
    draw_dependency(ax, admin_controller_pos['right'], user_service_pos['left'], None, 'dashed')
    
    # Draw dependencies - Services to Data Layer
    draw_dependency(ax, quiz_service_pos['bottom'], quiz_model_pos['right'], None, 'dashed')
    draw_dependency(ax, user_service_pos['bottom'], user_model_pos['right'], None, 'dashed')
    draw_dependency(ax, stats_service_pos['bottom'], quiz_model_pos['top'], None, 'dashed')
    draw_dependency(ax, stats_service_pos['bottom'], user_model_pos['top'], None, 'dashed')
    
    # Draw dependencies - Services to Databases
    draw_dependency(ax, quiz_service_pos['right'], quiz_db, "CRUD")
    draw_dependency(ax, user_service_pos['right'], user_db, "CRUD")
    
    # Add annotations for architecture layers
    ax.text(0.2, 5, "Presentation\nLayer", ha='center', va='center', fontsize=10, 
           rotation=90, fontweight='bold')
    ax.text(3.5, 5, "Controller\nLayer", ha='center', va='center', fontsize=10, 
           rotation=90, fontweight='bold')
    ax.text(6.5, 5, "Service\nLayer", ha='center', va='center', fontsize=10, 
           rotation=90, fontweight='bold')
    ax.text(10.5, 5, "Data\nStorage", ha='center', va='center', fontsize=10, 
           rotation=90, fontweight='bold')
    
    # Add title
    ax.set_title("Quiz Application Component Diagram", fontsize=14, pad=20)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/component_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Component diagram has been generated in docs/diagrams/output/component_diagram.png")

if __name__ == "__main__":
    generate_component_diagram() 