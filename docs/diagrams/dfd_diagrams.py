#!/usr/bin/env python
"""
Generate Data Flow Diagrams for the Quiz application.

This script creates Level 0, Level 1, and Level 2 Data Flow Diagrams
for the Quiz Application using matplotlib.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.path import Path

# Create output directory if it doesn't exist
os.makedirs('docs/diagrams/output', exist_ok=True)

# Define colors with enhanced scheme
PROCESS_COLOR = '#B3E5FC'  # Light blue
ENTITY_COLOR = '#FFECB3'   # Light amber
DATASTORE_COLOR = '#E1BEE7'  # Light purple
ARROW_COLOR = '#455A64'    # Darker blue-gray for better visibility
BACKGROUND_COLOR = '#FFFFFF'  # Pure white for better contrast
BORDER_COLOR = '#2C3E50'  # Dark blue-gray for borders

# Helper functions for drawing diagram elements
def draw_process(ax, x, y, width, height, name, level=0):
    """Draw a process (rounded rectangle) with text."""
    # Add subtle shadow for depth
    shadow = patches.FancyBboxPatch(
        (x + 0.05, y - 0.05), width, height,
        boxstyle=patches.BoxStyle("Round", pad=0.3),
        facecolor='#DDDDDD', edgecolor='none', alpha=0.5
    )
    ax.add_patch(shadow)
    
    # Draw the main process shape with enhanced styling
    process = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle=patches.BoxStyle("Round", pad=0.3),
        facecolor=PROCESS_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5
    )
    ax.add_patch(process)
    
    # Split name into lines if it contains \n
    lines = name.split('\n')
    line_height = height / (len(lines) + 1)
    
    for i, line in enumerate(lines):
        ax.text(x + width/2, y + height/2 + (len(lines)/2 - i - 0.5) * line_height,
                line, ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Add level indicator for processes (except Level 0)
    if level > 0:
        ax.text(x + width/2, y + height - 0.2, f"Process {level}",
                ha='center', va='top', fontsize=8, fontstyle='italic')
    
def draw_entity(ax, x, y, width, height, name):
    """Draw an external entity (rectangle) with text."""
    # Add subtle shadow for depth
    shadow = patches.Rectangle(
        (x + 0.05, y - 0.05), width, height,
        facecolor='#DDDDDD', edgecolor='none', alpha=0.5
    )
    ax.add_patch(shadow)
    
    # Draw the main entity with enhanced styling
    entity = patches.Rectangle(
        (x, y), width, height,
        facecolor=ENTITY_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5
    )
    ax.add_patch(entity)
    
    # Add entity label
    ax.text(x + width/2, y + height/2, name, 
            ha='center', va='center', fontsize=10, fontweight='bold')

def draw_datastore(ax, x, y, width, height, name):
    """Draw a data store (open-ended rectangle) with text."""
    # Add subtle shadow for depth
    shadow = patches.Rectangle(
        (x + 0.05, y - 0.05), width, height,
        facecolor='#DDDDDD', edgecolor='none', alpha=0.5
    )
    ax.add_patch(shadow)
    
    # Draw the main rectangle with enhanced styling
    datastore = patches.Rectangle(
        (x, y), width, height,
        facecolor=DATASTORE_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5
    )
    ax.add_patch(datastore)
    
    # Draw the left vertical line
    ax.plot([x, x], [y, y + height], color=BORDER_COLOR, linewidth=1.5)
    
    # Add datastore label
    ax.text(x + width/2, y + height/2, name, 
            ha='center', va='center', fontsize=10, fontweight='bold')

def calculate_bezier_points(start, end, control_scale=0.5):
    """Calculate points for a bezier curve between two points."""
    # Calculate control points
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    
    # Adjust control points based on direction
    if abs(dx) > abs(dy):  # Horizontal-ish flow
        control1 = (start[0] + dx * control_scale, start[1])
        control2 = (end[0] - dx * control_scale, end[1])
    else:  # Vertical-ish flow
        control1 = (start[0], start[1] + dy * control_scale)
        control2 = (end[0], end[1] - dy * control_scale)
    
    return control1, control2

def draw_arrow(ax, start, end, label="", midpoint_offset=(0, 0)):
    """Draw a curved arrow with a label."""
    # Calculate distance between points
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = np.sqrt(dx**2 + dy**2)
    
    # Adjust curvature based on distance
    curvature = min(0.3, distance * 0.15)
    
    # Determine if the flow is more horizontal or vertical
    if abs(dx) > abs(dy):
        # Horizontal flow - curve vertically
        # Adjust curve height based on direction to avoid crossing other elements
        curve_sign = -1 if start[1] > end[1] else 1
        control = (start[0] + dx/2, start[1] + dy/2 + curve_sign * curvature)
    else:
        # Vertical flow - curve horizontally
        # Adjust curve width based on direction to avoid crossing other elements
        curve_sign = -1 if start[0] > end[0] else 1
        control = (start[0] + dx/2 + curve_sign * curvature, start[1] + dy/2)
    
    # Create the curve points
    t = np.linspace(0, 1, 30)
    # Quadratic Bezier curve
    curve_x = (1-t)**2 * start[0] + 2*(1-t)*t * control[0] + t**2 * end[0]
    curve_y = (1-t)**2 * start[1] + 2*(1-t)*t * control[1] + t**2 * end[1]
    
    # Draw the curve with smoother line
    ax.plot(curve_x, curve_y, color=ARROW_COLOR, linewidth=1.8, solid_capstyle='round')
    
    # Calculate the direction at the end for the arrowhead
    # Use the last two points to determine direction
    end_direction = np.array([curve_x[-1] - curve_x[-2], curve_y[-1] - curve_y[-2]])
    end_direction = end_direction / np.linalg.norm(end_direction)
    
    # Add arrowhead
    arrow_length = 0.15
    arrow_width = 0.08
    
    # Calculate normal vector (perpendicular to direction)
    normal = np.array([-end_direction[1], end_direction[0]])
    
    # Calculate arrowhead points
    arrow_tip = np.array(end)
    arrow_base = arrow_tip - arrow_length * end_direction
    arrow_left = arrow_base + arrow_width * normal
    arrow_right = arrow_base - arrow_width * normal
    
    # Draw arrowhead with improved style
    arrow = patches.Polygon(
        [arrow_tip, arrow_left, arrow_right],
        facecolor=ARROW_COLOR,
        edgecolor='none',
        linewidth=1
    )
    ax.add_patch(arrow)
    
    # Calculate midpoint for label - adjust based on curve
    curve_midpoint_index = len(curve_x) // 2
    midpoint = np.array([
        curve_x[curve_midpoint_index] + midpoint_offset[0],
        curve_y[curve_midpoint_index] + midpoint_offset[1]
    ])
    
    # Add label with enhanced white background
    if label:
        ax.text(
            midpoint[0], midpoint[1],
            label,
            ha='center',
            va='center',
            fontsize=8,
            fontweight='bold',
            bbox=dict(
                facecolor='white',
                alpha=0.9,
                boxstyle='round,pad=0.3',
                edgecolor='#E0E0E0'
            )
        )

# Generate Level 0 DFD (Context Diagram)
def generate_level0_dfd():
    """Generate Level 0 DFD (Context Diagram)."""
    fig, ax = plt.subplots(figsize=(10, 6.5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw a subtle grid for better alignment (won't be visible in output)
    ax.grid(True, linestyle='--', alpha=0.1)
    
    # Draw the main process (the whole system) - centered
    draw_process(ax, 4, 2.25, 2.2, 2, "Quiz\nSystem")
    
    # Draw external entities - better positioned around the system
    draw_entity(ax, 0.8, 4.5, 1.5, 1, "User")
    draw_entity(ax, 7.7, 4.5, 1.5, 1, "Admin")
    draw_entity(ax, 0.8, 1, 1.5, 1, "Database")
    
    # Draw data flows with curved arrows - adjusted for better appearance
    draw_arrow(ax, (2.3, 4.75), (4, 3.75), "Quiz Request")
    draw_arrow(ax, (4.25, 2.25), (2.3, 1.5), "Data Query")
    draw_arrow(ax, (2.3, 1.25), (4, 2.5), "Data Response")
    draw_arrow(ax, (6.2, 3.75), (7.7, 4.75), "System Reports")
    draw_arrow(ax, (7.7, 4.25), (6.2, 3.25), "Admin Commands")
    draw_arrow(ax, (6.2, 2.5), (2.3, 4), "Quiz Results", (0, 0.25))
    
    # Add title with enhanced styling
    ax.set_title("Level 0 DFD: Quiz System Context Diagram", 
                 fontsize=16, pad=20, fontweight='bold', 
                 bbox=dict(facecolor='white', edgecolor='#E0E0E0', boxstyle='round,pad=0.5'))
    
    # Add subtle watermark
    fig.text(0.95, 0.05, "Quiz App", fontsize=12, color='lightgray', 
             ha='right', va='bottom', alpha=0.3, fontweight='bold')
    
    # Save the figure with higher quality
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/dfd_level0.png', dpi=300, bbox_inches='tight')
    plt.close()

# Generate Level 1 DFD
def generate_level1_dfd():
    """Generate Level 1 DFD showing main processes."""
    fig, ax = plt.subplots(figsize=(12, 8.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw subtle grid for better alignment (won't be visible in output)
    ax.grid(True, linestyle='--', alpha=0.1)
    
    # Draw external entities with improved spacing
    draw_entity(ax, 0.5, 6.5, 1.5, 1, "User")
    draw_entity(ax, 10, 6.5, 1.5, 1, "Admin")
    
    # Draw processes with more spacing and improved positioning
    draw_process(ax, 3, 6.5, 1.5, 1, "1. User\nAuthentication", 1)
    draw_process(ax, 3, 4.5, 1.5, 1, "2. Quiz\nSelection", 2)
    draw_process(ax, 6, 4.5, 1.5, 1, "3. Quiz\nTaking", 3)
    draw_process(ax, 6, 2.5, 1.5, 1, "4. Result\nAnalysis", 4)
    draw_process(ax, 9, 4.5, 1.5, 1, "5. Admin\nDashboard", 5)
    
    # Draw data stores with better spacing
    draw_datastore(ax, 1.5, 2.5, 2, 0.6, "D1: User Database")
    draw_datastore(ax, 4.5, 2.5, 2, 0.6, "D2: Question Database")
    draw_datastore(ax, 7.5, 2.5, 2, 0.6, "D3: Results Database")
    
    # Draw data flows with improved curves and spacing
    # User authentication flows
    draw_arrow(ax, (2, 7), (3, 7), "Login Request")
    draw_arrow(ax, (3.75, 6.5), (3, 2.8), "Verify User", (0.5, 0))
    draw_arrow(ax, (3, 2.5), (4.5, 6.5), "User Data", (0.5, 0))
    
    # Quiz selection flows
    draw_arrow(ax, (3.75, 7), (3.75, 5), "Authorized\nUser")
    draw_arrow(ax, (3.75, 4.5), (4.5, 2.8), "Query\nQuestions", (0, 0.3))
    draw_arrow(ax, (5.5, 2.8), (4, 4.5), "Available\nQuizzes", (0, 0.3))
    
    # Quiz taking flows
    draw_arrow(ax, (4.5, 5), (6, 5), "Selected\nQuiz")
    draw_arrow(ax, (6.75, 4.5), (6.75, 3), "Submit\nAnswers")
    
    # Result analysis flows
    draw_arrow(ax, (7.5, 2.8), (7.25, 2.5), "Store\nResults")
    draw_arrow(ax, (6.75, 2.5), (3, 6.5), "Show\nResults", (1, 0.5))
    
    # Admin flows
    draw_arrow(ax, (10, 7), (9, 5), "Admin\nLogin")
    draw_arrow(ax, (9, 4.5), (9.5, 2.8), "Manage\nData")
    draw_arrow(ax, (9, 4.5), (6.5, 2.8), "View\nStats", (-0.5, 0))
    
    # Add title with enhanced styling
    ax.set_title("Level 1 DFD: Quiz System Main Processes", 
                 fontsize=16, pad=20, fontweight='bold', 
                 bbox=dict(facecolor='white', edgecolor='#E0E0E0', boxstyle='round,pad=0.5'))
    
    # Add subtle watermark
    fig.text(0.95, 0.05, "Quiz App", fontsize=12, color='lightgray', 
             ha='right', va='bottom', alpha=0.3, fontweight='bold')
    
    # Save the figure with higher quality
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/dfd_level1.png', dpi=300, bbox_inches='tight')
    plt.close()

# Generate Level 2 DFD (focus on Quiz Taking process)
def generate_level2_dfd():
    """Generate Level 2 DFD detailing the Quiz Taking process."""
    fig, ax = plt.subplots(figsize=(12, 8.5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8.5)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw subtle grid for better alignment (won't be visible in output)
    ax.grid(True, linestyle='--', alpha=0.1)
    
    # Draw external entities
    draw_entity(ax, 0.5, 4.5, 1.5, 1, "User")
    
    # Draw parent process reference
    parent_process = patches.FancyBboxPatch(
        (0.5, 7), 11, 1,
        boxstyle=patches.BoxStyle("Round", pad=0.3),
        facecolor='#E8F5E9', edgecolor=BORDER_COLOR, linewidth=1.5
    )
    ax.add_patch(parent_process)
    ax.text(6, 7.5, "Process 3: Quiz Taking", 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Draw sub-processes with improved positioning
    draw_process(ax, 3, 4.5, 1.5, 1, "3.1\nLoad Quiz", 1)
    draw_process(ax, 6, 4.5, 1.5, 1, "3.2\nPresent\nQuestion", 2)
    draw_process(ax, 9, 4.5, 1.5, 1, "3.3\nProcess\nAnswer", 3)
    draw_process(ax, 6, 2.5, 1.5, 1, "3.4\nCalculate\nScore", 4)
    
    # Draw data stores with better spacing
    draw_datastore(ax, 3, 2.5, 2, 0.6, "D2: Question Database")
    draw_datastore(ax, 9, 2.5, 2, 0.6, "D3: Results Database")
    
    # Draw data flows with improved curves
    draw_arrow(ax, (2, 5), (3, 5), "Start Quiz")
    draw_arrow(ax, (3, 2.8), (3.75, 4.5), "Fetch Questions")
    draw_arrow(ax, (4.5, 5), (6, 5), "Quiz Data")
    draw_arrow(ax, (7.5, 5), (9, 5), "User Answer")
    draw_arrow(ax, (9.75, 4.5), (10, 2.8), "Store Answer")
    draw_arrow(ax, (9, 2.8), (7.5, 2.8), "Answer Data")
    draw_arrow(ax, (6.75, 2.5), (2, 4.8), "Final Score", (0, -0.5))
    
    # Add title with enhanced styling
    ax.set_title("Level 2 DFD: Quiz Taking Process Detail", 
                 fontsize=16, pad=20, fontweight='bold', 
                 bbox=dict(facecolor='white', edgecolor='#E0E0E0', boxstyle='round,pad=0.5'))
    
    # Add subtle watermark
    fig.text(0.95, 0.05, "Quiz App", fontsize=12, color='lightgray', 
             ha='right', va='bottom', alpha=0.3, fontweight='bold')
    
    # Save the figure with higher quality
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/dfd_level2.png', dpi=300, bbox_inches='tight')
    plt.close()

def generate_all_dfds():
    """Generate all DFD diagrams."""
    print("\nGenerating Level 0 DFD...")
    generate_level0_dfd()
    
    print("Generating Level 1 DFD...")
    generate_level1_dfd()
    
    print("Generating Level 2 DFD...")
    generate_level2_dfd()
    
    print("\nAll DFD diagrams have been generated successfully!")
    print("Output files saved to: docs/diagrams/output/dfd_level0.png, dfd_level1.png, dfd_level2.png")

if __name__ == "__main__":
    generate_all_dfds() 