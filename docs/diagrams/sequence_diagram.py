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
BORDER_COLOR = '#2C3E50'  # Dark blue-gray for borders

def draw_participant(ax, x, y, width, height, name, is_actor=False):
    """Draw a participant (actor or object) at the top of a sequence diagram."""
    if is_actor:
        # Draw actor with stick figure
        # Draw the head with proper facecolor/edgecolor instead of color
        head = plt.Circle((x + width/2, y + height - 0.3), 0.2, fill=True,
                          facecolor=ACTOR_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5)
        ax.add_patch(head)
        
        # Draw the body
        ax.plot([x + width/2, x + width/2], [y + height - 0.5, y + height - 0.8],
                color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
        
        # Draw the arms
        ax.plot([x + width/2 - 0.2, x + width/2 + 0.2], 
                [y + height - 0.6, y + height - 0.6], 
                color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
        
        # Draw the legs
        ax.plot([x + width/2, x + width/2 - 0.2], 
                [y + height - 0.8, y + height - 1.1], 
                color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
        ax.plot([x + width/2, x + width/2 + 0.2], 
                [y + height - 0.8, y + height - 1.1], 
                color=BORDER_COLOR, linewidth=2, solid_capstyle='round')
        
        # Draw name box with improved styling
        rect = patches.FancyBboxPatch(
            (x, y + height - 1.6), width, 0.4, 
            boxstyle=patches.BoxStyle("Round", pad=0.2),
            facecolor=ACTOR_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Add label with improved styling
        ax.text(x + width/2, y + height - 1.4, name, ha='center', va='center',
                fontsize=9, fontweight='bold')
    else:
        # Draw object box with improved styling
        # Add subtle shadow for depth
        shadow = patches.Rectangle((x + 0.03, y + height - 0.63), width, 0.6, fill=True,
                                  facecolor='#DDDDDD', edgecolor='none', alpha=0.5)
        ax.add_patch(shadow)
        
        # Draw the main box
        rect = patches.FancyBboxPatch(
            (x, y + height - 0.6), width, 0.6,
            boxstyle=patches.BoxStyle("Round", pad=0.2),
            facecolor=OBJECT_COLOR, edgecolor=BORDER_COLOR, linewidth=1.5
        )
        ax.add_patch(rect)
        
        # Add label with improved styling
        ax.text(x + width/2, y + height - 0.3, name, ha='center', va='center',
                fontsize=9, fontweight='bold')

def draw_lifeline(ax, x, y, height, bottom_y):
    """Draw a vertical dashed line representing an object's lifeline."""
    # Draw a subtle shadow for depth
    ax.plot([x + 0.02, x + 0.02], [y - 0.02, bottom_y - 0.02], 
           color='#DDDDDD', linestyle='--', linewidth=1, alpha=0.5)
    
    # Draw the main lifeline with improved styling
    ax.plot([x, x], [y, bottom_y], 
           color=LINE_COLOR, linestyle='--', linewidth=1.5, 
           dashes=(5, 3), alpha=0.8)

def draw_activation(ax, x, y_top, y_bottom, width=0.2):
    """Draw an activation box on a lifeline."""
    # Draw subtle shadow for depth
    shadow = patches.Rectangle((x - width/2 + 0.02, y_top - 0.02), width, y_bottom - y_top, 
                              fill=True, facecolor='#DDDDDD', edgecolor='none', alpha=0.5)
    ax.add_patch(shadow)
    
    # Draw the main activation box with improved styling
    rect = patches.FancyBboxPatch(
        (x - width/2, y_top), width, y_bottom - y_top, 
        boxstyle=patches.BoxStyle("Round", pad=0.02),
        facecolor=ACTIVATION_COLOR, edgecolor=BORDER_COLOR, linewidth=1
    )
    ax.add_patch(rect)

def draw_message(ax, start_x, start_y, end_x, end_y, name, is_return=False, is_self=False):
    """Draw a message arrow between lifelines with a label."""
    arrow_color = RETURN_COLOR if is_return else LINE_COLOR
    
    if is_self:
        # Self-message is drawn as a looping arrow with improved styling
        offset = 0.5
        # Draw the outgoing line with rounded caps
        ax.plot([start_x, start_x + offset], [start_y, start_y], 
               color=arrow_color, linewidth=1.5, solid_capstyle='round')
        # Draw the vertical line with rounded caps
        ax.plot([start_x + offset, start_x + offset], [start_y, end_y], 
               color=arrow_color, linewidth=1.5, solid_capstyle='round')
        
        # Calculate arrowhead
        arrow_length = 0.1
        arrow_width = 0.06
        
        # Add arrowhead with polygon for smoother appearance
        arrow_tip = (start_x, end_y)
        if is_return:
            # Return arrow points left
            direction = (-1, 0)
        else:
            # Normal arrow points right
            direction = (1, 0)
        
        normal = (-direction[1], direction[0])  # perpendicular vector
        
        arrow_base = (arrow_tip[0] - direction[0] * arrow_length, 
                      arrow_tip[1] - direction[1] * arrow_length)
        arrow_left = (arrow_base[0] + normal[0] * arrow_width,
                     arrow_base[1] + normal[1] * arrow_width)
        arrow_right = (arrow_base[0] - normal[0] * arrow_width,
                      arrow_base[1] - normal[1] * arrow_width)
        
        arrow = patches.Polygon(
            [arrow_tip, arrow_left, arrow_right],
            facecolor=arrow_color,
            edgecolor='none'
        )
        ax.add_patch(arrow)
        
        # Add label with improved styling
        ax.text(start_x + offset + 0.1, (start_y + end_y)/2, name, 
               ha='left', va='center', fontsize=8, fontweight='bold',
               bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.2', 
                       edgecolor='#E0E0E0'))
    else:
        # Regular message between different lifelines with curved arrow
        # Calculate a subtle curve
        t = np.linspace(0, 1, 30)
        dx = end_x - start_x
        dy = end_y - start_y
        distance = np.sqrt(dx**2 + dy**2)
        
        # Adjust curve height based on distance and direction
        curve_factor = min(0.1, distance * 0.05)
        curve_sign = -1 if start_y > end_y else 1
        
        if abs(dx) > abs(dy):
            # Horizontal message - subtle vertical curve
            control = (start_x + dx/2, start_y + dy/2 + curve_sign * curve_factor)
        else:
            # Vertical message - subtle horizontal curve
            control = (start_x + dx/2 + curve_sign * curve_factor, start_y + dy/2)
        
        # Create the Bezier curve
        curve_x = (1-t)**2 * start_x + 2*(1-t)*t * control[0] + t**2 * end_x
        curve_y = (1-t)**2 * start_y + 2*(1-t)*t * control[1] + t**2 * end_y
        
        # Draw the curve
        ax.plot(curve_x, curve_y, color=arrow_color, linewidth=1.5, solid_capstyle='round')
        
        # Calculate the direction at the end for the arrowhead
        end_direction = np.array([curve_x[-1] - curve_x[-2], curve_y[-1] - curve_y[-2]])
        end_direction = end_direction / np.linalg.norm(end_direction)
        
        # Add arrowhead
        arrow_length = 0.12
        arrow_width = 0.06
        
        # Calculate normal vector (perpendicular to direction)
        normal = np.array([-end_direction[1], end_direction[0]])
        
        # Calculate arrowhead points
        arrow_tip = np.array((end_x, end_y))
        arrow_base = arrow_tip - arrow_length * end_direction
        arrow_left = arrow_base + arrow_width * normal
        arrow_right = arrow_base - arrow_width * normal
        
        # Draw arrowhead
        arrow = patches.Polygon(
            [arrow_tip, arrow_left, arrow_right],
            facecolor=arrow_color,
            edgecolor='none'
        )
        ax.add_patch(arrow)
        
        # Add label with improved styling
        # Calculate midpoint based on curve
        midpoint_idx = len(curve_x) // 2
        midpoint_x = curve_x[midpoint_idx]
        midpoint_y = curve_y[midpoint_idx] + 0.1
        
        ax.text(midpoint_x, midpoint_y, name, ha='center', va='bottom',
                fontsize=8, fontweight='bold', color='black',
                bbox=dict(facecolor='white', alpha=0.9, boxstyle='round,pad=0.2', 
                        edgecolor='#E0E0E0'))

def generate_quiz_taking_sequence():
    """Generate a sequence diagram for the quiz-taking process."""
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.axis('off')
    ax.set_facecolor(BACKGROUND_COLOR)
    
    # Draw subtle grid for better alignment (won't be visible in output)
    ax.grid(True, linestyle='--', alpha=0.1)
    
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
        
        # UI displays next question or results
        {"from": 1, "to": 0, "y": 2.2, "name": "17: Show Next/Results", "is_return": True}
    ]
    
    # Draw messages
    for m in messages:
        if "is_self" in m and m["is_self"]:
            # Self-message
            p = participants[m["from"]]
            draw_message(ax, p["lifeline_x"], m["y_from"], p["lifeline_x"], m["y_to"], 
                       m["name"], is_return=False, is_self=True)
        else:
            # Regular message between participants
            p_from = participants[m["from"]]
            p_to = participants[m["to"]]
            draw_message(ax, p_from["lifeline_x"], m["y"], p_to["lifeline_x"], m["y"], 
                       m["name"], is_return=m.get("is_return", False))
    
    # Add a sequence numbering guide at the bottom
    guide_box = patches.FancyBboxPatch(
        (0.5, 0.3), 11, 0.5,
        boxstyle=patches.BoxStyle("Round", pad=0.2),
        facecolor='#F5F5F5', edgecolor=BORDER_COLOR, linewidth=1, alpha=0.8
    )
    ax.add_patch(guide_box)
    ax.text(6, 0.55, "Sequence numbers indicate the order of interactions in the quiz-taking flow", 
            ha='center', va='center', fontsize=9, fontweight='bold', fontstyle='italic')
    
    # Add title with enhanced styling
    ax.set_title("Quiz System Sequence Diagram: Quiz Taking Process", 
                 fontsize=16, pad=20, fontweight='bold', 
                 bbox=dict(facecolor='white', edgecolor='#E0E0E0', boxstyle='round,pad=0.5'))
    
    # Add subtle watermark
    fig.text(0.95, 0.05, "Quiz App", fontsize=12, color='lightgray', 
             ha='right', va='bottom', alpha=0.3, fontweight='bold')
    
    # Save the figure with higher quality
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/sequence_diagram.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Sequence diagram has been generated in docs/diagrams/output/sequence_diagram.png")

if __name__ == "__main__":
    generate_quiz_taking_sequence() 