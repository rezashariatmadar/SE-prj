#!/usr/bin/env python
"""
Generate Project Planning Diagrams for the Quiz application.

This script creates PERT and Gantt charts with three-point estimation
to illustrate the project planning process.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import networkx as nx
from datetime import datetime, timedelta
import matplotlib.dates as mdates

# Create output directory if it doesn't exist
os.makedirs('docs/diagrams/output', exist_ok=True)

# Define colors
NODE_COLOR = '#B3E5FC'  # Light blue
CRITICAL_COLOR = '#F44336'  # Red
GRID_COLOR = '#EEEEEE'  # Light gray
TEXT_COLOR = '#212121'  # Dark gray
BACKGROUND_COLOR = '#FAFAFA'  # Off-white
BAR_COLORS = ['#1976D2', '#388E3C', '#FBC02D', '#D32F2F', '#7B1FA2', '#0097A7']

# Define the tasks with three-point estimation
def create_task_data():
    """Create the task data with three-point estimates."""
    tasks = [
        {
            'id': 'A',
            'name': 'Requirements Analysis',
            'optimistic': 5,
            'most_likely': 7,
            'pessimistic': 10,
            'predecessors': []
        },
        {
            'id': 'B',
            'name': 'Database Design',
            'optimistic': 3,
            'most_likely': 5,
            'pessimistic': 8,
            'predecessors': ['A']
        },
        {
            'id': 'C',
            'name': 'User Interface Design',
            'optimistic': 4,
            'most_likely': 6,
            'pessimistic': 9,
            'predecessors': ['A']
        },
        {
            'id': 'D',
            'name': 'Model Development',
            'optimistic': 6,
            'most_likely': 8,
            'pessimistic': 12,
            'predecessors': ['B']
        },
        {
            'id': 'E',
            'name': 'View Development',
            'optimistic': 5,
            'most_likely': 7,
            'pessimistic': 10,
            'predecessors': ['C']
        },
        {
            'id': 'F',
            'name': 'Controller Development',
            'optimistic': 7,
            'most_likely': 10,
            'pessimistic': 14,
            'predecessors': ['D', 'E']
        },
        {
            'id': 'G',
            'name': 'Unit Testing',
            'optimistic': 3,
            'most_likely': 5,
            'pessimistic': 8,
            'predecessors': ['F']
        },
        {
            'id': 'H',
            'name': 'Integration Testing',
            'optimistic': 4,
            'most_likely': 6,
            'pessimistic': 9,
            'predecessors': ['G']
        },
        {
            'id': 'I',
            'name': 'Documentation',
            'optimistic': 3,
            'most_likely': 4,
            'pessimistic': 7,
            'predecessors': ['F']
        },
        {
            'id': 'J',
            'name': 'Deployment',
            'optimistic': 2,
            'most_likely': 3,
            'pessimistic': 5,
            'predecessors': ['H', 'I']
        }
    ]
    
    # Calculate expected time and variance for each task
    for task in tasks:
        # Expected time: (Optimistic + 4 * Most Likely + Pessimistic) / 6
        task['expected'] = round((task['optimistic'] + 4 * task['most_likely'] + task['pessimistic']) / 6, 1)
        
        # Standard deviation: (Pessimistic - Optimistic) / 6
        task['std_dev'] = round((task['pessimistic'] - task['optimistic']) / 6, 2)
        
        # Variance: Standard Deviation ^ 2
        task['variance'] = round(task['std_dev'] ** 2, 2)
    
    return tasks

def calculate_schedule(tasks):
    """Calculate earliest start, earliest finish, latest start, latest finish, and slack for each task."""
    # Copy tasks to avoid modifying the original
    schedule = tasks.copy()
    
    # Initialize time values
    for task in schedule:
        task['ES'] = 0
        task['EF'] = 0
        task['LS'] = float('inf')
        task['LF'] = float('inf')
        task['slack'] = 0
    
    # Forward pass - Calculate ES and EF
    changes = True
    while changes:
        changes = False
        for task in schedule:
            old_ef = task['EF']
            
            # ES = max of all predecessors' EF
            if task['predecessors']:
                task['ES'] = max([pred_task['EF'] for pred_task in schedule 
                                if pred_task['id'] in task['predecessors']])
            else:
                task['ES'] = 0
                
            # EF = ES + expected duration
            task['EF'] = task['ES'] + task['expected']
            
            if old_ef != task['EF']:
                changes = True
    
    # Find the project duration (maximum EF)
    project_duration = max([task['EF'] for task in schedule])
    
    # Backward pass - Calculate LS and LF
    for task in schedule:
        if not any(task['id'] in t['predecessors'] for t in schedule):
            # Terminal tasks
            task['LF'] = project_duration
        else:
            task['LF'] = float('inf')
    
    changes = True
    while changes:
        changes = False
        for task in reversed(schedule):
            old_ls = task['LS']
            
            # Find all successors
            successors = [succ_task for succ_task in schedule 
                         if task['id'] in succ_task['predecessors']]
            
            # LF = min of all successors' LS
            if successors:
                task['LF'] = min([succ_task['LS'] for succ_task in successors])
            else:
                task['LF'] = project_duration
                
            # LS = LF - expected duration
            task['LS'] = task['LF'] - task['expected']
            
            # Slack = LS - ES
            task['slack'] = task['LS'] - task['ES']
            
            if old_ls != task['LS']:
                changes = True
    
    # Mark critical path tasks
    for task in schedule:
        task['critical'] = (task['slack'] < 0.01)  # Allow for floating point imprecision
    
    return schedule, project_duration

def generate_three_point_table(tasks):
    """Generate a table visualization of the three-point estimation."""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    
    # Table data
    columns = ['Task ID', 'Task Name', 'Optimistic (O)', 'Most Likely (M)', 'Pessimistic (P)', 
               'Expected (E)', 'Std Dev (σ)', 'Variance (σ²)', 'Critical Path']
    
    # Create the table data
    table_data = []
    for task in tasks:
        critical = "✓" if task.get('critical', False) else ""
        table_data.append([
            task['id'],
            task['name'],
            task['optimistic'],
            task['most_likely'],
            task['pessimistic'],
            task['expected'],
            task['std_dev'],
            task['variance'],
            critical
        ])
    
    # Create table
    table = ax.table(
        cellText=table_data,
        colLabels=columns,
        cellLoc='center',
        loc='center',
        bbox=[0.0, 0.0, 1.0, 1.0]  # Use the full figure
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    
    # Set header style
    for i, key in enumerate(columns):
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#1976D2')  # Blue header
    
    # Style critical path tasks
    for i, task in enumerate(tasks):
        if task.get('critical', False):
            for j in range(len(columns)):
                cell = table[(i+1, j)]
                cell.set_facecolor('#FFECB3')  # Light amber highlight
    
    # Adjust column widths
    table.auto_set_column_width([0, 2, 3, 4, 5, 6, 7, 8])
    
    # Add title
    plt.suptitle('Three-Point Estimation Table', fontsize=14, y=0.95)
    
    # Add formula explanation
    formula_text = (
        "Three-Point Estimation Formula:\n"
        "Expected Time (E) = (O + 4M + P) / 6\n"
        "Standard Deviation (σ) = (P - O) / 6\n"
        "Variance (σ²) = σ²"
    )
    fig.text(0.02, 0.02, formula_text, fontsize=8, va='bottom')
    
    # Save the figure
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])  # Adjust layout to make room for title
    plt.savefig('docs/diagrams/output/three_point_estimation.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Three-point estimation table has been generated in docs/diagrams/output/three_point_estimation.png")

def generate_pert_chart(tasks, project_duration):
    """Generate a PERT chart using networkx."""
    # Create directed graph
    G = nx.DiGraph()
    
    # Add nodes
    for task in tasks:
        # Store the full name without abbreviation
        G.add_node(task['id'], 
                  # Remove the abbreviated ID from the label
                  full_name=task['name'],
                  duration=task['expected'],
                  es=task['ES'], 
                  ef=task['EF'], 
                  ls=task['LS'], 
                  lf=task['LF'], 
                  slack=task['slack'],
                  critical=task['critical'])
    
    # Add edges
    for task in tasks:
        for pred in task['predecessors']:
            G.add_edge(pred, task['id'])
    
    # Create the figure with more space at the bottom for the info boxes
    fig, ax = plt.subplots(figsize=(16, 14))
    
    # Set the layout - MODIFIED PARAMETERS for better node distribution
    # Increased k (repulsive force) to spread nodes out more
    # Increased iterations for better convergence
    pos = nx.spring_layout(G, k=0.3, iterations=100, seed=42)
    
    # Adjust position to leave space at the bottom for the info table
    # Move all nodes upward to create space at the bottom of the chart
    for node in pos:
        x, y = pos[node]
        # Compress the y-range to upper 70% of the plot
        pos[node] = (x, 0.15 + (y * 0.7))
    
    # Draw nodes
    critical_nodes = [n for n, attr in G.nodes(data=True) if attr['critical']]
    normal_nodes = [n for n in G.nodes() if n not in critical_nodes]
    
    # Draw edges with connectionstyle to reach only to the perimeter of the circles
    for edge in G.edges():
        source, target = edge
        start_pos, end_pos = pos[source], pos[target]
        # Use connectionstyle 'arc3' to make a straight line that stops at the perimeter
        ax.annotate("", xy=end_pos, xytext=start_pos,
                   arrowprops=dict(arrowstyle='->', color='black', 
                                  linewidth=1.5, shrinkA=15, shrinkB=15))
    
    # Draw regular nodes - INCREASED SIZE
    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=normal_nodes, 
                          node_color=NODE_COLOR, node_size=3000, alpha=0.9)
    
    # Draw critical path nodes - INCREASED SIZE
    nx.draw_networkx_nodes(G, pos, ax=ax, nodelist=critical_nodes, 
                          node_color=CRITICAL_COLOR, node_size=3000, alpha=0.9)
    
    # Add task ID labels inside each node
    for node, (x, y) in pos.items():
        ax.text(x, y, node, ha='center', va='center', fontsize=12, 
               color='white', fontweight='bold')
    
    # Add full task names closer to each node - position closer to the node edge
    for node, (x, y) in pos.items():
        node_data = G.nodes[node]
        full_name = node_data['full_name']
        duration = node_data['duration']
        # Position the text above the node but closer than before
        label = f"{node}: {full_name}\nDuration: {duration} days"
        ax.text(x, y+0.06, label, ha='center', va='center', fontsize=9, 
               bbox=dict(facecolor='white', alpha=0.8, boxstyle='round,pad=0.2', 
                         edgecolor='gray'), fontweight='bold')
    
    # Create a table at the bottom of the chart with all the task information
    table_data = []
    sorted_tasks = sorted(tasks, key=lambda t: t['id'])  # Sort by task ID
    
    # Create table headers
    columns = ['Task ID', 'Earliest Start', 'Earliest Finish', 'Latest Start', 'Latest Finish', 'Slack']
    
    # Create the table data
    for task in sorted_tasks:
        table_data.append([
            task['id'],
            f"{task['ES']:.1f}",
            f"{task['EF']:.1f}",
            f"{task['LS']:.1f}",
            f"{task['LF']:.1f}",
            f"{task['slack']:.1f}"
        ])
    
    # Create a table at the bottom of the chart
    # Position the table at the bottom of the chart, centered horizontally
    table = ax.table(
        cellText=table_data,
        colLabels=columns,
        cellLoc='center',
        loc='bottom',
        bbox=[0.1, -0.3, 0.8, 0.2]  # [left, bottom, width, height]
    )
    
    # Style the table
    table.auto_set_font_size(False)
    table.set_fontsize(9)
    
    # Style header row
    for i, key in enumerate(columns):
        cell = table[(0, i)]
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#1976D2')  # Blue header
    
    # Style critical path tasks
    for i, task in enumerate(sorted_tasks):
        if task.get('critical', False):
            for j in range(len(columns)):
                cell = table[(i+1, j)]
                cell.set_facecolor('#FFECB3')  # Light amber highlight
    
    # Add a title to the table
    ax.text(0.5, -0.05, "Task Schedule Information", 
            ha='center', va='center', fontsize=12, fontweight='bold', 
            transform=ax.transAxes)
    
    # Add legend - IMPROVED POSITIONING
    critical_patch = patches.Patch(color=CRITICAL_COLOR, label='Critical Path')
    normal_patch = patches.Patch(color=NODE_COLOR, label='Normal Task')
    ax.legend(handles=[critical_patch, normal_patch], loc='upper right', fontsize=12)
    
    # Add title - INCREASED FONT SIZE
    ax.set_title(f"PERT Chart - Project Duration: {project_duration:.1f} days", fontsize=16, pad=20)
    
    # Turn off axis
    ax.axis('off')
    
    # Save the figure - ADDED BETTER PADDING
    plt.tight_layout(pad=2.0)
    plt.savefig('docs/diagrams/output/pert_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("PERT chart has been generated in docs/diagrams/output/pert_chart.png")

def generate_gantt_chart(tasks):
    """Generate a Gantt chart with three-point estimation error bars."""
    # Sort tasks by early start
    sorted_tasks = sorted(tasks, key=lambda x: x['ES'])
    
    # Create a figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Configure the axis
    ax.set_facecolor(BACKGROUND_COLOR)
    ax.grid(True, axis='x', linestyle='--', linewidth=0.5, color=GRID_COLOR)
    
    # Create task bars
    y_ticks = []
    y_labels = []
    
    for i, task in enumerate(sorted_tasks):
        # Position on y-axis
        y_pos = len(sorted_tasks) - i
        y_ticks.append(y_pos)
        y_labels.append(f"{task['id']}: {task['name']}")
        
        # Draw the task bar
        color_idx = i % len(BAR_COLORS)
        if task['critical']:
            edgecolor = CRITICAL_COLOR
            linewidth = 2
        else:
            edgecolor = BAR_COLORS[color_idx]
            linewidth = 1
        
        # Calculate positions
        left = task['ES']
        width = task['expected']
        
        # Draw main bar with expected duration
        ax.barh(y_pos, width, left=left, height=0.5,
                color=BAR_COLORS[color_idx], alpha=0.7,
                edgecolor=edgecolor, linewidth=linewidth)
        
        # Add task label inside bar
        if width >= 2:  # Only add text inside bar if it's wide enough
            ax.text(left + width/2, y_pos, task['id'], 
                    ha='center', va='center', color='white', fontweight='bold')
        else:
            ax.text(left + width + 0.1, y_pos, task['id'], 
                    ha='left', va='center', color=TEXT_COLOR)
        
        # Add error bars for three-point estimation
        min_time = task['optimistic']
        max_time = task['pessimistic']
        ax.hlines(y_pos, left + min_time, left + max_time, colors='black', linestyles='-', linewidth=1)
        ax.vlines(left + min_time, y_pos - 0.1, y_pos + 0.1, colors='black', linestyles='-', linewidth=1)
        ax.vlines(left + max_time, y_pos - 0.1, y_pos + 0.1, colors='black', linestyles='-', linewidth=1)
        
        # Add dependency arrows
        for pred_id in task['predecessors']:
            # Find predecessor task
            pred_task = next((t for t in sorted_tasks if t['id'] == pred_id), None)
            if pred_task:
                pred_y_pos = len(sorted_tasks) - sorted_tasks.index(pred_task)
                pred_end = pred_task['ES'] + pred_task['expected']
                
                # Draw arrow from predecessor end to task start
                ax.annotate('', xy=(task['ES'], y_pos), xytext=(pred_end, pred_y_pos),
                           arrowprops=dict(arrowstyle='->', color='gray', 
                                         linewidth=1, linestyle=':',
                                         connectionstyle='arc3,rad=0.3'))
    
    # Set y-ticks and labels
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_labels)
    
    # Set x-axis label and limits
    ax.set_xlabel('Time (days)')
    max_ef = max([task['EF'] for task in tasks])
    ax.set_xlim(0, max_ef * 1.1)  # Add some padding on the right
    
    # Add legend
    critical_patch = patches.Patch(color=CRITICAL_COLOR, label='Critical Path Task Border')
    normal_patch = patches.Patch(color=BAR_COLORS[0], label='Task Duration')
    error_line = plt.Line2D([0], [0], color='black', linewidth=1, linestyle='-', label='Min/Max Duration')
    ax.legend(handles=[normal_patch, critical_patch, error_line], loc='upper right')
    
    # Add grid on the y-axis
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, linestyle='--', linewidth=0.5, color=GRID_COLOR)
    
    # Add title
    ax.set_title("Gantt Chart with Three-Point Estimation", fontsize=14, pad=20)
    
    # Invert y-axis
    ax.invert_yaxis()
    
    # Save the figure
    plt.tight_layout()
    plt.savefig('docs/diagrams/output/gantt_chart.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Gantt chart has been generated in docs/diagrams/output/gantt_chart.png")

def generate_all_planning_diagrams():
    """Generate all project planning diagrams."""
    # Create task data
    tasks = create_task_data()
    
    # Calculate schedule
    scheduled_tasks, project_duration = calculate_schedule(tasks)
    
    # Generate diagrams
    generate_three_point_table(scheduled_tasks)
    generate_pert_chart(scheduled_tasks, project_duration)
    generate_gantt_chart(scheduled_tasks)
    
    print("All project planning diagrams have been generated.")

if __name__ == "__main__":
    generate_all_planning_diagrams() 