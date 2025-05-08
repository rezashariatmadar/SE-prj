"""
Generate example analytics visualizations for documentation.

This script creates realistic example visualizations that show how the 
analytics features look with sample data. These images can be used in 
the documentation to give users a clear understanding of the analytics features.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
import os
from datetime import datetime, timedelta
import random

# Create directory for example images
output_dir = 'docs/_static/analytics_examples'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the style for all charts
sns.set_style('whitegrid')
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'legend.fontsize': 12,
    'figure.titlesize': 18
})

# 1. Performance Over Time Chart
# Generate dates for the last 3 months
dates = [(datetime.now() - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(90, 0, -5)]

# Generate fake data for 3 categories
categories = ['Science', 'History', 'Mathematics']
data = []

for date in dates:
    for category in categories:
        # Generate a score that generally improves over time with some randomness
        index = dates.index(date)
        base_score = 70 + (index / len(dates)) * 20  # Scores improve from ~70 to ~90
        
        if category == 'Science':
            # Science starts strong and stays strong
            score = base_score + random.uniform(-5, 5)
        elif category == 'History':
            # History starts weaker but improves more
            score = base_score - 10 + (index / len(dates)) * 15 + random.uniform(-5, 5)
        else:
            # Mathematics is most variable
            score = base_score - 5 + random.uniform(-10, 10)
            
        # Ensure score is within 0-100
        score = max(min(score, 100), 0)
        
        data.append({
            'date': date,
            'category': category,
            'score_percentage': score
        })

# Create DataFrame
df = pd.DataFrame(data)

# Create the visualization
plt.figure(figsize=(12, 6))
ax = sns.lineplot(data=df, x='date', y='score_percentage', hue='category', marker='o', linewidth=2.5)
plt.title('Quiz Performance Over Time', fontweight='bold', pad=20)
plt.xlabel('Date', fontweight='bold')
plt.ylabel('Score (%)', fontweight='bold')
plt.ylim(0, 100)
plt.xticks(rotation=45, ha='right')
plt.grid(True, alpha=0.3)
plt.legend(title='Category', title_fontsize=12)
plt.tight_layout()
plt.savefig(f'{output_dir}/performance_time.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"Generated: performance_time.png")

# 2. Performance by Category Chart
category_perf = df.groupby('category')['score_percentage'].mean().sort_values(ascending=False)
plt.figure(figsize=(10, 6))
ax = sns.barplot(x=category_perf.index, y=category_perf.values, palette='viridis')
for i, v in enumerate(category_perf.values):
    ax.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
plt.title('Average Performance by Category', fontweight='bold', pad=20)
plt.xlabel('Category', fontweight='bold')
plt.ylabel('Average Score (%)', fontweight='bold')
plt.ylim(0, 105)
overall_avg = df['score_percentage'].mean()
plt.axhline(y=overall_avg, color='red', linestyle='--', label=f'Overall Avg: {overall_avg:.1f}%')
plt.legend()
plt.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(f'{output_dir}/performance_category.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"Generated: performance_category.png")

# 3. Quiz Length Distribution Chart
quiz_lengths = [5, 10, 15, 20]
quiz_counts = [15, 25, 10, 5]  # Most quizzes are 10 questions
plt.figure(figsize=(8, 6))
plt.pie(quiz_counts, labels=[f'{count} questions' for count in quiz_lengths], 
        autopct='%1.1f%%', startangle=90, shadow=True, 
        wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
        textprops={'fontsize': 12, 'fontweight': 'bold'})
plt.title('Quiz Length Distribution', fontweight='bold', pad=20)
plt.axis('equal')
plt.savefig(f'{output_dir}/quiz_distribution.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"Generated: quiz_distribution.png")

# 4. Performance by Difficulty (for results page)
difficulties = ['easy', 'medium', 'hard']
difficulty_scores = [85, 72, 58]  # Typical pattern: better on easy, worse on hard
plt.figure(figsize=(8, 4))
ax = sns.barplot(x=difficulties, y=difficulty_scores, palette='YlOrRd')
for i, v in enumerate(difficulty_scores):
    ax.text(i, v + 2, f'{v:.1f}%', ha='center', fontweight='bold')
plt.title('Performance by Question Difficulty', fontweight='bold')
plt.xlabel('Difficulty Level', fontweight='bold')
plt.ylabel('Correct Answers (%)', fontweight='bold')
plt.ylim(0, 100)
plt.grid(axis='y', alpha=0.3)
plt.savefig(f'{output_dir}/difficulty_performance.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"Generated: difficulty_performance.png")

# 5. User dashboard summary view
plt.figure(figsize=(12, 8))

# Create 2x2 grid for charts
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# Chart 1: Performance over time (simplified)
sns.lineplot(data=df, x='date', y='score_percentage', hue='category', ax=ax1, marker='o')
ax1.set_title('Performance Over Time', fontweight='bold')
ax1.set_xlabel('Date')
ax1.set_ylabel('Score (%)')
ax1.set_ylim(0, 100)
ax1.tick_params(axis='x', rotation=45)
ax1.legend(title='Category')

# Chart 2: Category performance
sns.barplot(x=category_perf.index, y=category_perf.values, ax=ax2, palette='viridis')
ax2.set_title('Performance by Category', fontweight='bold')
ax2.set_xlabel('Category')
ax2.set_ylabel('Avg. Score (%)')
ax2.set_ylim(0, 100)

# Chart 3: Quiz distribution
ax3.pie(quiz_counts, labels=[f'{count} Q' for count in quiz_lengths], autopct='%1.1f%%', 
        startangle=90, wedgeprops={'linewidth': 1, 'edgecolor': 'white'})
ax3.set_title('Quiz Length Distribution', fontweight='bold')
ax3.axis('equal')

# Chart 4: Recent quiz scores
recent_scores = [76, 82, 65, 90, 78]
recent_dates = [(datetime.now() - timedelta(days=x)).strftime('%m/%d') for x in range(25, 0, -5)]
sns.barplot(x=recent_dates, y=recent_scores, ax=ax4, palette='Blues_d')
ax4.set_title('Recent Quiz Scores', fontweight='bold')
ax4.set_xlabel('Date')
ax4.set_ylabel('Score (%)')
ax4.set_ylim(0, 100)

plt.tight_layout()
plt.savefig(f'{output_dir}/dashboard_summary.png', dpi=100, bbox_inches='tight')
plt.close()
print(f"Generated: dashboard_summary.png")

print(f"All example analytics visualizations saved to {output_dir}") 