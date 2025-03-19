#!/usr/bin/env python
"""
Question Population Script for Quiz Application

This script adds a large number of questions to each category in the database.
It uses Django's ORM to interact with the database and create questions and choices.

Usage:
    python manage.py shell < scripts/populate_questions.py
    
    Or run directly with Django environment:
    python scripts/populate_questions.py
"""

import os
import sys
import random
import django

# Set up Django environment if script is run directly
if __name__ == "__main__":
    # Add the parent directory to sys.path
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "quiz_project.settings")
    django.setup()

# Import the models
from quiz_app.models import Category, Question, Choice
from django.db import transaction

# Configuration
QUESTIONS_PER_CATEGORY = 50  # Number of questions to create per category
CHOICES_PER_QUESTION = 4     # Number of choices per question

# Question templates for different categories
QUESTION_TEMPLATES = {
    'Science': [
        "What is {element} on the periodic table?",
        "Which scientist discovered {discovery}?",
        "What is the scientific name for {common_name}?",
        "In what year was {discovery} discovered?",
        "What is the function of {organ} in the human body?",
        "Which of the following is NOT a {category}?",
        "What is {theory} theory about?",
        "Which law of physics explains {phenomenon}?",
        "What is the formula for {compound}?",
        "How many {unit} are in a {larger_unit}?",
    ],
    'History': [
        "Who was the leader of {country} during {event}?",
        "In what year did {event} occur?",
        "Which civilization first developed {invention}?",
        "What was the significance of the {treaty}?",
        "Who was responsible for {achievement}?",
        "Which battle ended the {war}?",
        "What caused the {event} to happen?",
        "Where was {person} born?",
        "Which empire controlled {region} during the {century} century?",
        "What was {person}'s contribution to {field}?",
    ],
    'Geography': [
        "What is the capital of {country}?",
        "Which country has the largest {feature}?",
        "Where is {landmark} located?",
        "Which continent contains {country}?",
        "What is the highest mountain in {region}?",
        "Which river flows through {city}?",
        "What type of climate does {region} have?",
        "Which ocean borders {country}?",
        "What is the population of {city}?",
        "Which countries border {country}?",
    ],
    'Literature': [
        "Who wrote '{book}'?",
        "Which character appears in '{book}'?",
        "In what year was '{book}' published?",
        "What is the main theme of '{book}'?",
        "Which literary movement does {author} belong to?",
        "What is the setting of '{book}'?",
        "Who is the protagonist in '{book}'?",
        "Which of the following is NOT written by {author}?",
        "What type of narrative is used in '{book}'?",
        "Which award did '{book}' win?",
    ],
    'Sports': [
        "Which team won the {championship} in {year}?",
        "Who holds the record for {achievement} in {sport}?",
        "What is the scoring system in {sport}?",
        "Where were the {year} Olympics held?",
        "Which country has won the most {championship}?",
        "What equipment is used in {sport}?",
        "How many players are on a {sport} team?",
        "What is the duration of a {sport} match?",
        "Which {sport} position is responsible for {task}?",
        "When was {sport} first included in the Olympics?",
    ],
    'Technology': [
        "Who invented the {invention}?",
        "When was {technology} first introduced?",
        "What programming language is used for {application}?",
        "What does {acronym} stand for in technology?",
        "Which company developed {product}?",
        "What is the purpose of {technology}?",
        "How does {technology} work?",
        "Which of these is NOT a {category}?",
        "What was the predecessor to {technology}?",
        "What operating system uses {feature}?",
    ],
}

# Sample data for question templates
SAMPLE_DATA = {
    'Science': {
        'element': ['Hydrogen', 'Oxygen', 'Carbon', 'Nitrogen', 'Gold', 'Silver', 'Iron', 'Helium', 'Neon', 'Calcium'],
        'discovery': ['Penicillin', 'DNA structure', 'Radioactivity', 'X-rays', 'Gravity', 'Evolution', 'Quantum theory', 'Electromagnetism', 'Vaccination', 'Cell theory'],
        'common_name': ['dog', 'house cat', 'human', 'fruit fly', 'yeast', 'corn', 'rice', 'potato', 'tomato', 'oak tree'],
        'organ': ['heart', 'lungs', 'liver', 'kidneys', 'brain', 'stomach', 'pancreas', 'small intestine', 'large intestine', 'skin'],
        'category': ['mammal', 'reptile', 'bird', 'amphibian', 'fish', 'invertebrate', 'plant', 'fungus', 'bacterium', 'virus'],
        'theory': ['evolution', 'relativity', 'quantum', 'big bang', 'cell', 'germ', 'plate tectonics', 'heliocentric', 'atomic', 'string'],
        'phenomenon': ['gravity', 'magnetism', 'light refraction', 'sound waves', 'buoyancy', 'thermal expansion', 'radioactivity', 'electricity', 'fluid dynamics', 'inertia'],
        'compound': ['water', 'carbon dioxide', 'sodium chloride', 'glucose', 'methane', 'ethanol', 'ammonia', 'sulfuric acid', 'nitric acid', 'hydrochloric acid'],
        'unit': ['milliliters', 'grams', 'centimeters', 'seconds', 'joules', 'watts', 'volts', 'amperes', 'kelvins', 'moles'],
        'larger_unit': ['liter', 'kilogram', 'meter', 'minute', 'kilojoule', 'kilowatt', 'kilovolt', 'kiloampere', 'degree', 'kilomole'],
    },
    'History': {
        'country': ['United States', 'United Kingdom', 'France', 'Germany', 'Russia', 'China', 'Japan', 'Italy', 'Spain', 'Egypt'],
        'event': ['World War I', 'World War II', 'French Revolution', 'Industrial Revolution', 'Cold War', 'American Revolution', 'Russian Revolution', 'Renaissance', 'Great Depression', 'Civil Rights Movement'],
        'invention': ['writing', 'wheel', 'printing press', 'steam engine', 'electricity', 'gunpowder', 'compass', 'antibiotics', 'internet', 'nuclear power'],
        'treaty': ['Treaty of Versailles', 'Treaty of Paris', 'Treaty of Westphalia', 'Treaty of Rome', 'Treaty of Tordesillas', 'Treaty of Ghent', 'Treaty of Nanking', 'Treaty of Brest-Litovsk', 'SALT Treaty', 'NATO'],
        'achievement': ['Moon landing', 'mapping the human genome', 'first heart transplant', 'invention of television', 'first computer', 'discovery of penicillin', 'splitting the atom', 'four-minute mile', 'construction of the Panama Canal', 'circumnavigation of the globe'],
        'war': ['Hundred Years War', 'American Civil War', 'Napoleonic Wars', 'Vietnam War', 'Korean War', 'Gulf War', 'Thirty Years War', 'Crimean War', 'Boer War', 'Spanish-American War'],
        'person': ['Napoleon Bonaparte', 'Alexander the Great', 'Julius Caesar', 'Cleopatra', 'Genghis Khan', 'Christopher Columbus', 'Leonardo da Vinci', 'Marie Curie', 'Albert Einstein', 'Mahatma Gandhi'],
        'region': ['Europe', 'Middle East', 'Asia', 'Africa', 'North America', 'South America', 'Australia', 'Mediterranean', 'Scandinavia', 'Balkans'],
        'century': ['15th', '16th', '17th', '18th', '19th', '20th', '1st', '5th', '10th', '12th'],
        'field': ['science', 'mathematics', 'philosophy', 'literature', 'art', 'music', 'medicine', 'law', 'engineering', 'politics'],
    },
    'Geography': {
        'country': ['France', 'Brazil', 'Japan', 'Australia', 'Egypt', 'Canada', 'India', 'Mexico', 'South Africa', 'Italy'],
        'feature': ['desert', 'rainforest', 'coral reef', 'mountain range', 'river', 'lake', 'island', 'peninsula', 'delta', 'canyon'],
        'landmark': ['Eiffel Tower', 'Great Wall of China', 'Machu Picchu', 'Taj Mahal', 'Pyramids of Giza', 'Grand Canyon', 'Stonehenge', 'Statue of Liberty', 'Colosseum', 'Great Barrier Reef'],
        'region': ['Europe', 'South America', 'East Asia', 'Middle East', 'North Africa', 'Scandinavia', 'Central America', 'Caribbean', 'Southeast Asia', 'Oceania'],
        'city': ['Paris', 'Tokyo', 'New York', 'Cairo', 'Rio de Janeiro', 'Moscow', 'Sydney', 'Cape Town', 'Mexico City', 'Mumbai'],
    },
    'Literature': {
        'book': ['To Kill a Mockingbird', '1984', 'Pride and Prejudice', 'The Great Gatsby', 'Moby Dick', 'War and Peace', 'Don Quixote', 'Hamlet', 'The Odyssey', 'The Catcher in the Rye'],
        'author': ['William Shakespeare', 'Jane Austen', 'Charles Dickens', 'Leo Tolstoy', 'Ernest Hemingway', 'Virginia Woolf', 'Mark Twain', 'George Orwell', 'F. Scott Fitzgerald', 'Gabriel García Márquez'],
    },
    'Sports': {
        'championship': ['World Cup', 'Super Bowl', 'NBA Finals', 'World Series', 'Stanley Cup', 'Wimbledon', 'Masters Tournament', 'Olympics', 'UEFA Champions League', 'Grand Prix'],
        'year': ['2022', '2018', '2014', '2010', '2006', '2002', '1998', '1994', '1990', '1986'],
        'achievement': ['most goals', 'highest score', 'fastest time', 'most wins', 'longest winning streak', 'most championships', 'most Olympic medals', 'most points in a season', 'most consecutive wins', 'highest batting average'],
        'sport': ['soccer', 'basketball', 'tennis', 'golf', 'baseball', 'hockey', 'volleyball', 'swimming', 'track and field', 'skiing'],
        'task': ['scoring', 'defending', 'passing', 'goalkeeping', 'serving', 'rebounding', 'pitching', 'catching', 'blocking', 'shooting'],
    },
    'Technology': {
        'invention': ['computer', 'internet', 'smartphone', 'television', 'transistor', 'microprocessor', 'laser', 'digital camera', 'GPS', 'WiFi'],
        'technology': ['artificial intelligence', 'blockchain', 'cloud computing', 'virtual reality', 'augmented reality', '5G', 'quantum computing', 'machine learning', 'Internet of Things', 'big data'],
        'application': ['web development', 'mobile apps', 'game development', 'data analysis', 'system programming', 'scientific computing', 'embedded systems', 'artificial intelligence', 'database management', 'cybersecurity'],
        'acronym': ['HTML', 'CPU', 'RAM', 'URL', 'API', 'SQL', 'HTTP', 'IoT', 'AI', 'GPS'],
        'product': ['iPhone', 'Windows', 'Gmail', 'Photoshop', 'Office 365', 'Android', 'Chrome', 'AWS', 'PlayStation', 'Tesla Autopilot'],
        'category': ['smartphone', 'laptop', 'tablet', 'smartwatch', 'game console', 'e-reader', 'smart speaker', 'fitness tracker', 'VR headset', 'drone'],
        'feature': ['touch screen', 'facial recognition', 'voice commands', 'cloud sync', 'wireless charging', 'biometric security', 'gesture control', 'augmented reality', 'split-screen multitasking', 'night mode'],
    },
}

def generate_question_text(category_name):
    """Generate a random question text for a given category."""
    if category_name in QUESTION_TEMPLATES:
        template = random.choice(QUESTION_TEMPLATES[category_name])
        
        # Extract placeholders from the template using simple string processing
        placeholders = []
        i = 0
        while True:
            start = template.find('{', i)
            if start == -1:
                break
            end = template.find('}', start)
            if end == -1:
                break
            placeholder = template[start+1:end]
            placeholders.append(placeholder)
            i = end + 1
        
        # Fill in placeholders with sample data
        filled_template = template
        for placeholder in placeholders:
            if placeholder in SAMPLE_DATA.get(category_name, {}):
                value = random.choice(SAMPLE_DATA[category_name][placeholder])
                filled_template = filled_template.replace(f"{{{placeholder}}}", value)
        
        return filled_template
    else:
        return f"Sample question for {category_name} category #{random.randint(1, 1000)}"

def generate_answer_choices(category_name, correct_answer=None):
    """Generate a list of answer choices, ensuring one is correct."""
    # Simple generic answers if no category-specific ones
    choices = []
    
    if not correct_answer:
        correct_answer = f"Answer {random.randint(1, 100)}"
    
    choices.append(correct_answer)
    
    # Generate incorrect answers
    for i in range(CHOICES_PER_QUESTION - 1):
        incorrect_answer = f"Incorrect answer {random.randint(1, 1000)}"
        while incorrect_answer in choices:
            incorrect_answer = f"Incorrect answer {random.randint(1, 1000)}"
        choices.append(incorrect_answer)
    
    # Shuffle the choices
    random.shuffle(choices)
    
    return choices, choices.index(correct_answer)

def generate_explanation(question_text):
    """Generate an explanation for a question."""
    explanations = [
        f"The correct answer can be found by analyzing the key concepts in {question_text}.",
        f"This question tests your knowledge of fundamental principles related to the topic.",
        f"Understanding the context of this question is crucial to selecting the right answer.",
        f"The answer follows from the basic definitions in this subject area.",
        f"This question requires applying theoretical knowledge to a specific example.",
    ]
    return random.choice(explanations)

def create_questions_for_category(category, num_questions):
    """Create a specified number of questions for a category."""
    questions_created = 0
    
    for _ in range(num_questions):
        # Generate question text
        question_text = generate_question_text(category.name)
        
        # Generate an explanation
        explanation = generate_explanation(question_text)
        
        # Get difficulty
        difficulty = random.choice(['easy', 'medium', 'hard'])
        
        # Create the question
        question = Question.objects.create(
            category=category,
            text=question_text,
            explanation=explanation,
            difficulty=difficulty
        )
        
        # Generate choices and mark one as correct
        choices, correct_index = generate_answer_choices(category.name)
        
        # Create the choices
        for i, choice_text in enumerate(choices):
            Choice.objects.create(
                question=question,
                text=choice_text,
                is_correct=(i == correct_index)
            )
        
        questions_created += 1
        
    return questions_created

def main():
    """Main function to populate the database with questions."""
    # Get all categories
    categories = Category.objects.all()
    
    if not categories.exists():
        print("No categories found. Please create categories first.")
        return
    
    total_questions = 0
    
    # Use a transaction for efficiency and to ensure atomicity
    with transaction.atomic():
        for category in categories:
            # Check if the category already has questions
            existing_count = Question.objects.filter(category=category).count()
            
            if existing_count >= QUESTIONS_PER_CATEGORY:
                print(f"Category '{category.name}' already has {existing_count} questions. Skipping.")
                continue
            
            # Calculate how many more questions to add
            questions_to_add = QUESTIONS_PER_CATEGORY - existing_count
            
            if questions_to_add > 0:
                questions_created = create_questions_for_category(category, questions_to_add)
                total_questions += questions_created
                print(f"Added {questions_created} questions to category '{category.name}'")
    
    print(f"\nSuccessfully added {total_questions} questions across {categories.count()} categories.")
    print(f"Each category now has at least {QUESTIONS_PER_CATEGORY} questions.")

if __name__ == "__main__":
    main() 