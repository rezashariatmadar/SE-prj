"""
Script to generate placeholder images for documentation.

This script creates placeholder images for the documentation where 
real screenshots are not available yet.
"""

import os
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Ensure _static directory exists
static_dir = Path('_static')
static_dir.mkdir(exist_ok=True)

def create_placeholder(filename, title, width=800, height=600, 
                       bg_color=(245, 245, 245), text_color=(70, 70, 70)):
    """Create a placeholder image with a title."""
    img = Image.new('RGB', (width, height), color=bg_color)
    draw = ImageDraw.Draw(img)
    
    # Try to use a system font, fallback to default if not available
    try:
        # For Windows
        font_path = "C:\\Windows\\Fonts\\Arial.ttf"
        if os.path.exists(font_path):
            title_font = ImageFont.truetype(font_path, 40)
            subtitle_font = ImageFont.truetype(font_path, 30)
        else:
            # Use default font
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    except IOError:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    
    # Add title
    text_width, text_height = draw.textsize(title, font=title_font) if hasattr(draw, 'textsize') else (300, 40)
    position = ((width - text_width) // 2, (height - text_height) // 3)
    draw.text(position, title, font=title_font, fill=text_color)
    
    # Add placeholder text
    subtitle = "Placeholder Image"
    sub_width, sub_height = draw.textsize(subtitle, font=subtitle_font) if hasattr(draw, 'textsize') else (200, 30)
    sub_position = ((width - sub_width) // 2, (height - sub_height) // 2)
    draw.text(sub_position, subtitle, font=subtitle_font, fill=text_color)
    
    # Add border
    border_width = 2
    for i in range(border_width):
        draw.rectangle(
            [(i, i), (width - i - 1, height - i - 1)],
            outline=(200, 200, 200)
        )
    
    # Save the image
    img.save(static_dir / filename)
    print(f"Created placeholder image: {filename}")

# Create application screenshot placeholders
placeholders = [
    ('quiz_game_logo.png', 'Quiz Game Logo', 400, 200),
    ('homepage_screenshot.png', 'Quiz Game Homepage'),
    ('start_quiz_screenshot.png', 'Quiz Selection'),
    ('question_screenshot.png', 'Quiz Question'),
    ('results_screenshot.png', 'Quiz Results'),
    ('stats_screenshot.png', 'User Statistics'),
    ('architecture_diagram.png', 'Application Architecture', 900, 500),
    ('view_flow_diagram.png', 'View Flow Diagram', 900, 500),
]

# Generate each placeholder
for args in placeholders:
    create_placeholder(*args)

print("All placeholder images have been created successfully!") 