"""
Script to generate placeholder images for documentation.

This script creates placeholder images for the documentation where 
real screenshots are not available yet.

Why are placeholder images needed?
----------------------------------
Documentation looks better with images, but sometimes we don't have the real
screenshots ready (especially during development). These placeholder images:
- Make the documentation look complete
- Show where real images will eventually go
- Provide meaningful examples of charts for understanding analytics features

This script automatically creates all the needed images so we don't have to make them manually.
"""

import os
import matplotlib.pyplot as plt  # For creating charts
import numpy as np  # For working with numerical data
from PIL import Image, ImageDraw, ImageFont  # For creating and editing images
from pathlib import Path  # For working with file paths in a platform-independent way

# Ensure _static directory exists (this is where Sphinx documentation looks for images)
static_dir = Path('_static')
static_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist (do nothing if it already exists)

def create_placeholder(filename, title, width=800, height=600, 
                       bg_color=(245, 245, 245), text_color=(70, 70, 70)):
    """
    Create a placeholder image with a title.
    
    This function:
    1. Creates a blank image with the specified dimensions and background color
    2. Adds the title and "Placeholder Image" text
    3. Draws a border around the image
    4. Saves the image to the static directory
    
    Parameters:
    - filename: Name to save the image as (e.g., 'homepage.png')
    - title: Title text to display on the image
    - width/height: Image dimensions in pixels
    - bg_color: Background color as RGB tuple
    - text_color: Text color as RGB tuple
    """
    # Create a new blank image with the specified background color
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)  # Create a drawing object to add text and shapes
    
    # Try to use a nice font if available, or fall back to the default font
    try:
        # For Windows - try to use Arial font if available
        font_path = "C:\\Windows\\Fonts\\Arial.ttf"
        if os.path.exists(font_path):
            title_font = ImageFont.truetype(font_path, 40)  # Large font for title
            subtitle_font = ImageFont.truetype(font_path, 30)  # Medium font for subtitle
        else:
            # Use default font if Arial not available
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    except IOError:
        # Fallback if there's an error loading fonts
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Add the title text to the top part of the image
    # We need to handle different versions of PIL which have different APIs
    text_width, text_height = draw.textsize(title, font=title_font) if hasattr(draw, 'textsize') else (300, 40)
    position = ((width - text_width) // 2, (height - text_height) // 3)  # Center horizontally, position in top third
    draw.text(position, title, font=title_font, fill=text_color)
    
    # Add "Placeholder Image" text to the middle of the image
    subtitle = "Placeholder Image"
    sub_width, sub_height = draw.textsize(subtitle, font=subtitle_font) if hasattr(draw, 'textsize') else (200, 30)
    sub_position = ((width - sub_width) // 2, (height - sub_height) // 2)  # Center horizontally and vertically
    draw.text(sub_position, subtitle, font=subtitle_font, fill=text_color)
    
    # Add a border around the image to make it look more polished
    border_width = 2
    for i in range(border_width):
        draw.rectangle(
            [(i, i), (width - i - 1, height - i - 1)],  # Draw rectangle from top-left to bottom-right
            outline=(200, 200, 200)  # Light gray border
        )
    
    # Save the image to the static directory
    img.save(static_dir / filename)
    print(f"Created placeholder image: {filename}")

def create_example_analytics_chart(filename, chart_type):
    """
    Create example analytics charts for documentation.
    
    This function creates realistic-looking example charts for the analytics
    documentation, so readers can understand what the actual charts will look like.
    
    Parameters:
    - filename: Name to save the chart as (e.g., 'performance_chart.png')
    - chart_type: Type of chart to create ('time', 'category', or 'distribution')
    """
    # Create a new figure for the chart with a good size for documentation
    plt.figure(figsize=(10, 6))
    
    if chart_type == 'time':
        # Create a sample performance over time chart (line chart)
        # This chart shows how a user's scores change over time by category
        
        np.random.seed(42)  # For reproducibility - makes the random numbers the same every time
        
        # Create sample data - dates and scores for two categories
        dates = np.array(['2023-01-01', '2023-01-15', '2023-02-01', '2023-02-15', 
                          '2023-03-01', '2023-03-15', '2023-04-01'])
        scores_cat1 = np.random.randint(60, 100, size=len(dates))  # Random scores between 60-100
        scores_cat2 = np.random.randint(50, 95, size=len(dates))   # Random scores between 50-95
        
        # Plot two lines, one for each category, with markers at each data point
        plt.plot(dates, scores_cat1, 'o-', label='Science', linewidth=2)
        plt.plot(dates, scores_cat2, 'o-', label='History', linewidth=2)
        
        # Add title and labels
        plt.title('Performance Over Time', fontsize=16, fontweight='bold')
        plt.xlabel('Date', fontsize=12)
        plt.ylabel('Score (%)', fontsize=12)
        plt.ylim(0, 100)  # Set y-axis range from 0-100%
        
        # Add grid and rotate date labels for better readability
        plt.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()  # Adjust spacing to make sure everything fits
        
    elif chart_type == 'category':
        # Create a sample category performance chart (bar chart)
        # This chart shows average performance across different quiz categories
        
        # Create sample data - categories and their average scores
        categories = ['Science', 'History', 'Math', 'Literature', 'Geography']
        scores = np.random.randint(60, 95, size=len(categories))  # Random scores between 60-95
        
        # Create bar chart
        plt.bar(categories, scores, color='skyblue')
        
        # Add a horizontal line for the overall average score
        plt.axhline(y=np.mean(scores), color='red', linestyle='--', 
                   label=f'Average: {np.mean(scores):.1f}%')
        
        # Add title and labels
        plt.title('Performance by Category', fontsize=16, fontweight='bold')
        plt.xlabel('Category', fontsize=12)
        plt.ylabel('Average Score (%)', fontsize=12)
        plt.ylim(0, 100)  # Set y-axis range from 0-100%
        
        # Add grid on y-axis only and rotate category labels
        plt.grid(axis='y', alpha=0.3)
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        
    elif chart_type == 'distribution':
        # Create a sample quiz length distribution chart (pie chart)
        # This chart shows what proportion of quizzes had different numbers of questions
        
        # Create sample data - number of quizzes with different question counts
        sizes = [15, 10, 25, 5]  # Count of quizzes with each length
        labels = ['5 questions', '10 questions', '15 questions', '20 questions']
        explode = (0, 0.1, 0, 0)  # Slightly separate the second slice for emphasis
        
        # Create pie chart with percentage labels, shadow, and a starting angle
        plt.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
        plt.title('Quiz Length Distribution', fontsize=16, fontweight='bold')
        
    # Save the chart to an image file
    plt.savefig(static_dir / filename, dpi=100, bbox_inches='tight')
    plt.close()  # Close the plot to free up memory
    print(f"Created analytics chart: {filename}")

# List of all placeholder images we need to create
# Each entry is: (filename, title, [optional width], [optional height])
placeholders = [
    ('quiz_game_logo.png', 'Quiz Game Logo', 400, 200),
    ('homepage_screenshot.png', 'Quiz Game Homepage'),
    ('start_quiz_screenshot.png', 'Quiz Selection'),
    ('question_screenshot.png', 'Quiz Question'),
    ('results_screenshot.png', 'Quiz Results'),
    ('stats_screenshot.png', 'User Statistics'),
    ('architecture_diagram.png', 'Application Architecture', 900, 500),
    ('view_flow_diagram.png', 'View Flow Diagram', 900, 500),
    ('analytics_dashboard.png', 'Analytics Dashboard'),
    ('analytics_feature_diagram.png', 'Analytics Feature Overview', 900, 500),
]

# Generate each placeholder image in the list
for args in placeholders:
    create_placeholder(*args)  # The * unpacks the tuple into separate arguments

# Create the example analytics charts
create_example_analytics_chart('time_chart_example.png', 'time')
create_example_analytics_chart('category_chart_example.png', 'category')
create_example_analytics_chart('question_dist_example.png', 'distribution')

print("All placeholder images have been created successfully!") 