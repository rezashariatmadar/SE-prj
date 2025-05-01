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

# Define colors
PROCESS_COLOR = '#B3E5FC'  # Light blue
ENTITY_COLOR = '#FFECB3'   # Light amber
DATASTORE_COLOR = '#E1BEE7'  # Light purple
ARROW_COLOR = '#616161'    # Dark gray
BACKGROUND_COLOR = '#FAFAFA'  # Off-white

# Helper functions for drawing diagram elements
def draw_process(ax, x, y, width, height, name, level=0):
    """Draw a process (rounded rectangle) with text."""
    process = patches.FancyBboxPatch(
        (x, y), width, height,
        boxstyle=patches.BoxStyle("Round", pad=0.3),
        facecolor=PROCESS_COLOR, edgecolor='black', linewidth=1
    )
    ax.add_patch(process)
    
    # Add process label
    ax.text(x + width/2, y + height/2, name, 
            ha='center', va='center', fontsize=10, fontweight='bold')
    
    # Add level indicator for processes (except Level 0)
    if level > 0:
        ax.text(x + width/2, y + height - 0.2, f"Process {level}",
                ha='center', va='top', fontsize=8, fontstyle='italic')
    
def draw_entity(ax, x, y, width, height, name):
    """Draw an external entity (rectangle) with text."""
    entity = patches.Rectangle(
        (x, y), width, height,
        facecolor=ENTITY_COLOR, edgecolor='black', linewidth=1
    )
    ax.add_patch(entity)
    
    # Add entity label
    ax.text(x + width/2, y + height/2, name, 
            ha='center', va='center', fontsize=10, fontweight='bold')

def draw_datastore(ax, x, y, width, height, name):
    """Draw a data store (open-ended rectangle) with text."""
    # Draw the main rectangle
    datastore = patches.Rectangle(
        (x, y), width, height,
        facecolor=DATASTORE_COLOR, edgecolor='black', linewidth=1
    )
    ax.add_patch(datastore)
    
    # Draw the left vertical line
    ax.plot([x, x], [y, y + height], color='black', linewidth=1)
    
    # Add datastore label
    ax.text(x + width/2, y + height/2, name, 
            ha='center', va='center', fontsize=10, fontweight='bold')

def draw_arrow(ax, start, end, label="", midpoint_offset=(0, 0)):
    """Draw a directed arrow with a label."""
    # Calculate midpoint for label placement
    midpoint = ((start[0] + end[0]) / 2 + midpoint_offset[0], 
                (start[1] + end[1]) / 2 + midpoint_offset[1])
    
    # Draw arrow
    ax.annotate("", xy=end, xytext=start,
                arrowprops=dict(arrowstyle="->", color=ARROW_COLOR, 
                                lw=1.5, connectionstyle="arc3,rad=0.1"))
    
    # Add label if provided
    if label:
        ax.text(midpoint[0], midpoint[1], label, 
                ha='center', va='center', fontsize=8,
                bbox=dict(facecolor='white', alpha=0.7, boxstyle='round,pad=0.2', edgecolor='none'))

# Generate Level 0 DFD (Context Diagram)
def generate_level0_dfd():
    """Generate Level 0 DFD (Context Diagram)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw the main process (the whole system)
    draw_process(ax, 4, 2, 2, 2, "Quiz\nSystem")
    
    # Draw external entities
    draw_entity(ax, 1, 4, 1.5, 1, "User")
    draw_entity(ax, 8, 4, 1.5, 1, "Admin")
    draw_entity(ax, 1, 1, 1.5, 1, "Database")
    
    # Draw data flows
    draw_arrow(ax, (2.5, 4.5), (4, 3.5), "Quiz Request")
    draw_arrow(ax, (4, 3), (2.5, 1.5), "Data Query")
    draw_arrow(ax, (2.5, 1), (4, 2.5), "Data Response")
    draw_arrow(ax, (6, 3.5), (8, 4.5), "System Reports")
    draw_arrow(ax, (8, 4), (6, 3), "Admin Commands")
    draw_arrow(ax, (6, 2.5), (2.5, 4), "Quiz Results")
    
    # Add title
    ax.set_title("Level 0 DFD: Quiz System Context Diagram", fontsize=14, pad=20)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/dfd_level0.png', dpi=300, bbox_inches='tight')
    plt.close()

# Generate Level 1 DFD
def generate_level1_dfd():
    """Generate Level 1 DFD showing main processes."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw external entities
    draw_entity(ax, 0.5, 6, 1.5, 1, "User")
    draw_entity(ax, 10, 6, 1.5, 1, "Admin")
    
    # Draw processes
    draw_process(ax, 3, 6, 1.5, 1, "1. User\nAuthentication", 1)
    draw_process(ax, 3, 4, 1.5, 1, "2. Quiz\nSelection", 2)
    draw_process(ax, 6, 4, 1.5, 1, "3. Quiz\nTaking", 3)
    draw_process(ax, 6, 2, 1.5, 1, "4. Result\nAnalysis", 4)
    draw_process(ax, 9, 4, 1.5, 1, "5. Admin\nDashboard", 5)
    
    # Draw data stores
    draw_datastore(ax, 1.5, 2, 2, 0.6, "D1: User Database")
    draw_datastore(ax, 4.5, 2, 2, 0.6, "D2: Question Database")
    draw_datastore(ax, 7.5, 2, 2, 0.6, "D3: Results Database")
    
    # Draw data flows
    # User authentication flows
    draw_arrow(ax, (2, 6.5), (3, 6.5), "Login Request")
    draw_arrow(ax, (3.75, 6), (3, 2.3), "Verify User", (0.5, 0))
    draw_arrow(ax, (3, 2), (4.5, 6), "User Data", (0.5, 0))
    
    # Quiz selection flows
    draw_arrow(ax, (3.75, 6.5), (3.75, 4.5), "Authorized\nUser")
    draw_arrow(ax, (3.75, 4), (4.5, 2.3), "Query\nQuestions", (0, 0.3))
    draw_arrow(ax, (5.5, 2.3), (4, 4), "Available\nQuizzes", (0, 0.3))
    
    # Quiz taking flows
    draw_arrow(ax, (4.5, 4.5), (6, 4.5), "Selected\nQuiz")
    draw_arrow(ax, (6.75, 4), (6.75, 2.5), "Submit\nAnswers")
    
    # Result analysis flows
    draw_arrow(ax, (7.5, 2.3), (7.25, 2), "Store\nResults")
    draw_arrow(ax, (6.75, 2), (3, 6), "Show\nResults", (1, 0.5))
    
    # Admin flows
    draw_arrow(ax, (10, 6.5), (9, 4.5), "Admin\nLogin")
    draw_arrow(ax, (9, 4), (9.5, 2.3), "Manage\nData")
    draw_arrow(ax, (9, 4), (6.5, 2.3), "View\nStats", (-0.5, 0))
    
    # Add title
    ax.set_title("Level 1 DFD: Quiz System Main Processes", fontsize=14, pad=20)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/dfd_level1.png', dpi=300, bbox_inches='tight')
    plt.close()

# Generate Level 2 DFD (focus on Quiz Taking process)
def generate_level2_dfd():
    """Generate Level 2 DFD detailing the Quiz Taking process."""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw external entities
    draw_entity(ax, 0.5, 4, 1.5, 1, "User")
    
    # Draw parent process reference
    parent_process = patches.FancyBboxPatch(
        (0.5, 6.5), 11, 1,
        boxstyle=patches.BoxStyle("Round", pad=0.3),
        facecolor='#E8F5E9', edgecolor='black', linewidth=1
    )
    ax.add_patch(parent_process)
    ax.text(6, 7, "Process 3: Quiz Taking", 
            ha='center', va='center', fontsize=12, fontweight='bold')
    
    # Draw processes
    draw_process(ax, 3, 4, 1.5, 1, "3.1 Question\nRetrieval", 3.1)
    draw_process(ax, 6, 4, 1.5, 1, "3.2 Answer\nSubmission", 3.2)
    draw_process(ax, 9, 4, 1.5, 1, "3.3 Progress\nTracking", 3.3)
    draw_process(ax, 6, 2, 1.5, 1, "3.4 Score\nCalculation", 3.4)
    
    # Draw data stores
    draw_datastore(ax, 3, 1.5, 2, 0.6, "D2: Question Database")
    draw_datastore(ax, 8, 1.5, 2, 0.6, "D3: Results Database")
    
    # Draw data flows
    # Question retrieval
    draw_arrow(ax, (2, 4.5), (3, 4.5), "Request\nQuestion")
    draw_arrow(ax, (3.75, 4), (4, 1.8), "Fetch\nQuestion")
    draw_arrow(ax, (3.5, 1.5), (3.5, 3.8), "Question\nData")
    
    # Answer submission
    draw_arrow(ax, (4.5, 4.5), (6, 4.5), "Display\nQuestion")
    draw_arrow(ax, (6.75, 4), (7.5, 4.5), "User\nAnswer")
    
    # Progress tracking
    draw_arrow(ax, (9, 4), (9, 1.8), "Update\nProgress")
    draw_arrow(ax, (7.5, 4), (6.75, 3), "Track\nResponse")
    
    # Score calculation
    draw_arrow(ax, (9, 3.5), (7.2, 2.5), "Quiz\nCompletion")
    draw_arrow(ax, (6, 2), (8, 1.8), "Store\nFinal Score")
    draw_arrow(ax, (5.5, 2.5), (2, 4), "Display\nResults", (-0.5, 0))
    
    # Add title
    ax.set_title("Level 2 DFD: Quiz Taking Process Detail", fontsize=14, pad=20)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/dfd_level2.png', dpi=300, bbox_inches='tight')
    plt.close()

# Generate all DFDs
def generate_all_dfds():
    """Generate all three levels of DFD diagrams."""
    print("Generating Level 0 DFD...")
    generate_level0_dfd()
    
    print("Generating Level 1 DFD...")
    generate_level1_dfd()
    
    print("Generating Level 2 DFD...")
    generate_level2_dfd()
    
    print("All DFD diagrams have been generated in docs/diagrams/output/")

if __name__ == "__main__":
    generate_all_dfds() 