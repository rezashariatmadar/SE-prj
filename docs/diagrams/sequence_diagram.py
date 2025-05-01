#!/usr/bin/env python
"""
Generate Sequence Diagram for the Quiz application.

This script creates a UML sequence diagram for the quiz-taking flow
using matplotlib.
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Create output directory if it doesn't exist
os.makedirs('docs/diagrams/output', exist_ok=True)

# Define colors
ACTOR_COLOR = '#FFD580'  # Light orange
OBJECT_COLOR = '#B3E5FC'  # Light blue
ACTIVATION_COLOR = '#BBDEFB'  # Lighter blue
RETURN_COLOR = '#4CAF50'  # Green
LINE_COLOR = '#616161'  # Dark gray
BACKGROUND_COLOR = '#FAFAFA'  # Off-white

def draw_participant(ax, x, y, width, height, name, is_actor=False):
    """Draw a participant (actor or object) at the top of a sequence diagram."""
    if is_actor:
        # Draw actor with stick figure
        # Draw the head
        head = plt.Circle((x + width/2, y + height - 0.3), 0.2, fill=True,
                          color=ACTOR_COLOR, edgecolor='black', linewidth=1)
        ax.add_patch(head)
        
        # Draw the body
        ax.plot([x + width/2, x + width/2], [y + height - 0.5, y + height - 0.8],
                color='black', linewidth=2)
        
        # Draw the arms
        ax.plot([x + width/2 - 0.2, x + width/2 + 0.2], 
                [y + height - 0.6, y + height - 0.6], color='black', linewidth=2)
        
        # Draw the legs
        ax.plot([x + width/2, x + width/2 - 0.2], 
                [y + height - 0.8, y + height - 1.1], color='black', linewidth=2)
        ax.plot([x + width/2, x + width/2 + 0.2], 
                [y + height - 0.8, y + height - 1.1], color='black', linewidth=2)
        
        # Draw name box
        rect = patches.Rectangle((x, y + height - 1.6), width, 0.4, fill=True,
                                facecolor=ACTOR_COLOR, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        
        # Add label
        ax.text(x + width/2, y + height - 1.4, name, ha='center', va='center',
                fontsize=9, fontweight='bold')
    else:
        # Draw object box
        rect = patches.Rectangle((x, y + height - 0.6), width, 0.6, fill=True,
                                facecolor=OBJECT_COLOR, edgecolor='black', linewidth=1)
        ax.add_patch(rect)
        
        # Add label
        ax.text(x + width/2, y + height - 0.3, name, ha='center', va='center',
                fontsize=9, fontweight='bold')

def draw_lifeline(ax, x, y, height, bottom_y):
    """Draw a vertical dashed line representing an object's lifeline."""
    ax.plot([x, x], [y, bottom_y], color=LINE_COLOR, linestyle='--', linewidth=1)

def draw_activation(ax, x, y_top, y_bottom, width=0.2):
    """Draw an activation box on a lifeline."""
    rect = patches.Rectangle((x - width/2, y_top), width, y_bottom - y_top, fill=True,
                            facecolor=ACTIVATION_COLOR, edgecolor='black', linewidth=1)
    ax.add_patch(rect)

def draw_message(ax, start_x, start_y, end_x, end_y, name, is_return=False, is_self=False):
    """Draw a message arrow between lifelines with a label."""
    if is_self:
        # Self-message is drawn as a looping arrow
        arrow_style = '<-' if is_return else '->'
        offset = 0.5
        # Draw the outgoing line
        ax.annotate('', xy=(start_x + offset, start_y), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle='-', color=LINE_COLOR, lw=1.5))
        # Draw the horizontal line
        ax.plot([start_x + offset, start_x + offset], [start_y, end_y], color=LINE_COLOR, linewidth=1.5)
        # Draw the incoming arrow
        ax.annotate('', xy=(start_x, end_y), xytext=(start_x + offset, end_y),
                   arrowprops=dict(arrowstyle=arrow_style, color=RETURN_COLOR if is_return else LINE_COLOR, lw=1.5))
        
        # Add label
        ax.text(start_x + offset + 0.1, (start_y + end_y)/2, name, ha='left', va='center',
                fontsize=8, color='black')
    else:
        # Regular message between different lifelines
        arrow_style = '<-' if is_return else '->'
        arrow_color = RETURN_COLOR if is_return else LINE_COLOR
        
        ax.annotate('', xy=(end_x, end_y), xytext=(start_x, start_y),
                   arrowprops=dict(arrowstyle=arrow_style, color=arrow_color, lw=1.5))
        
        # Add label
        midpoint_x = (start_x + end_x) / 2
        ax.text(midpoint_x, start_y + 0.1, name, ha='center', va='bottom',
                fontsize=8, color='black')

def generate_quiz_taking_sequence():
    """Generate a sequence diagram for the quiz-taking process."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Define participants with positions
    participants = [
        {"name": "User", "x": 1, "width": 1.5, "is_actor": True},
        {"name": "Browser UI", "x": 3.5, "width": 1.5, "is_actor": False},
        {"name": "Quiz Controller", "x": 6, "width": 1.5, "is_actor": False},
        {"name": "Question Model", "x": 8.5, "width": 1.5, "is_actor": False},
        {"name": "Database", "x": 11, "width": 1.5, "is_actor": False}
    ]
    
    # Calculate positions
    top_y = 9
    bottom_y = 1
    participant_height = 1.6
    
    # Draw participants and lifelines
    for p in participants:
        draw_participant(ax, p["x"], top_y - participant_height, p["width"], participant_height, 
                        p["name"], p["is_actor"])
        lifeline_x = p["x"] + p["width"]/2
        draw_lifeline(ax, lifeline_x, top_y - participant_height, participant_height, bottom_y)
        p["lifeline_x"] = lifeline_x  # Store lifeline x position for messages
    
    # Define activation periods
    activations = [
        # Browser UI activations
        {"participant": 1, "y_top": 7.5, "y_bottom": 2},
        # Quiz Controller activations
        {"participant": 2, "y_top": 7.2, "y_bottom": 2.5},
        # Question Model activations
        {"participant": 3, "y_top": 6.7, "y_bottom": 3.0},
        {"participant": 3, "y_top": 5.0, "y_bottom": 4.5},
        # Database activations
        {"participant": 4, "y_top": 6.4, "y_bottom": 6.0},
        {"participant": 4, "y_top": 3.5, "y_bottom": 3.2}
    ]
    
    # Draw activations
    for a in activations:
        p = participants[a["participant"]]
        draw_activation(ax, p["lifeline_x"], a["y_top"], a["y_bottom"])
    
    # Define message flows
    messages = [
        # User selects a quiz category
        {"from": 0, "to": 1, "y": 7.5, "name": "1: Select Quiz Category", "is_return": False},
        
        # UI requests quiz data from controller
        {"from": 1, "to": 2, "y": 7.2, "name": "2: Request Quiz Data", "is_return": False},
        
        # Controller fetches questions from model
        {"from": 2, "to": 3, "y": 6.7, "name": "3: Fetch Questions", "is_return": False},
        
        # Model queries database
        {"from": 3, "to": 4, "y": 6.4, "name": "4: Query Database", "is_return": False},
        {"from": 4, "to": 3, "y": 6.0, "name": "5: Return Question Data", "is_return": True},
        
        # Model returns questions to controller
        {"from": 3, "to": 2, "y": 5.5, "name": "6: Return Questions", "is_return": True},
        
        # Controller sends quiz to UI
        {"from": 2, "to": 1, "y": 5.2, "name": "7: Initialize Quiz", "is_return": True},
        
        # UI displays first question
        {"from": 1, "to": 0, "y": 4.9, "name": "8: Display Question", "is_return": True},
        
        # User answers question
        {"from": 0, "to": 1, "y": 4.5, "name": "9: Submit Answer", "is_return": False},
        
        # UI validates answer
        {"from": 1, "to": 1, "y_from": 4.3, "y_to": 4.0, "name": "10: Validate", "is_self": True},
        
        # UI processes answer with controller
        {"from": 1, "to": 2, "y": 3.8, "name": "11: Process Answer", "is_return": False},
        
        # Controller updates model
        {"from": 2, "to": 3, "y": 3.5, "name": "12: Update Response", "is_return": False},
        
        # Model stores in database
        {"from": 3, "to": 4, "y": 3.3, "name": "13: Save Response", "is_return": False},
        {"from": 4, "to": 3, "y": 3.0, "name": "14: Confirm Save", "is_return": True},
        
        # Model confirms to controller
        {"from": 3, "to": 2, "y": 2.8, "name": "15: Response Recorded", "is_return": True},
        
        # Controller returns next question or results
        {"from": 2, "to": 1, "y": 2.5, "name": "16: Next Question/Results", "is_return": True},
        
        # UI shows next question or results
        {"from": 1, "to": 0, "y": 2.2, "name": "17: Display Next/Results", "is_return": True}
    ]
    
    # Draw messages
    for m in messages:
        from_participant = participants[m["from"]]
        to_participant = participants[m["to"]]
        start_x = from_participant["lifeline_x"]
        end_x = to_participant["lifeline_x"]
        
        if "is_self" in m and m["is_self"]:
            # Self-message
            draw_message(ax, start_x, m["y_from"], end_x, m["y_to"], 
                        m["name"], is_return=m.get("is_return", False), is_self=True)
        else:
            # Regular message
            draw_message(ax, start_x, m["y"], end_x, m["y"], 
                        m["name"], is_return=m.get("is_return", False))
    
    # Add title
    ax.set_title("Sequence Diagram: Quiz Taking Process", fontsize=14, pad=20)
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/sequence_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Sequence diagram has been generated in docs/diagrams/output/sequence_diagram.png")

if __name__ == "__main__":
    generate_quiz_taking_sequence() 