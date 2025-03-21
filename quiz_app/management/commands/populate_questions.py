"""
Management command to populate the database with quiz questions.

This command generates a specified number of quiz questions for each category in the database.
It creates varied question content and randomizes the correct answers to avoid predictable patterns.
"""

import random
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from quiz_app.models import Category, Question, Choice

class Command(BaseCommand):
    """Command to populate quiz questions."""
    
    help = 'Populates the database with a specified number of questions for each category'
    
    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--questions-per-category',
            type=int,
            default=10,
            help='Number of questions to generate per category'
        )
        parser.add_argument(
            '--choices-per-question',
            type=int,
            default=4,
            help='Number of choices per question'
        )
    
    def handle(self, *args, **options):
        """Execute the command."""
        questions_per_category = options['questions_per_category']
        choices_per_question = options['choices_per_question']
        
        # Get categories
        categories = Category.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create categories first.'))
            return
        
        # Generate questions
        try:
            with transaction.atomic():
                for category in categories:
                    self.generate_questions_for_category(
                        category, 
                        questions_per_category, 
                        choices_per_question
                    )
                    
                self.stdout.write(self.style.SUCCESS(f'Successfully generated {questions_per_category} questions for each category'))
                
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating questions: {str(e)}'))
    
    def generate_questions_for_category(self, category, count, choices_count):
        """Generate questions for a specific category."""
        self.stdout.write(f'Generating {count} questions for category: {category.name}')
        
        # Get template questions for each category
        templates = self.get_question_templates(category.name)
        
        # Check if we have enough templates
        if len(templates) < count:
            self.stdout.write(self.style.WARNING(
                f'Only {len(templates)} question templates available for {category.name}. '
                f'Some questions will be reused.'
            ))
        
        # Generate questions
        existing_questions = Question.objects.filter(category=category).count()
        for i in range(count):
            # Select a template (repeat if necessary)
            template = templates[i % len(templates)]
            
            # Generate question text
            question_text = self.generate_question_text(template, i + existing_questions)
            
            # Create the question
            difficulty = random.choice(['easy', 'medium', 'hard'])
            explanation = f"Explanation for {question_text}"
            
            question = Question.objects.create(
                category=category,
                text=question_text,
                explanation=explanation,
                difficulty=difficulty
            )
            
            # Generate choices with randomized position for correct answer
            self.generate_choices(question, template, choices_count)
            
            self.stdout.write(f'  Created question: {question_text[:50]}...')
    
    def generate_question_text(self, template, index):
        """Generate question text from a template."""
        if isinstance(template, dict) and 'format' in template:
            # Format the template with specific values
            format_str = template['format']
            values = template.get('values', [])
            value_index = index % len(values) if values else 0
            value = values[value_index] if values else index
            
            if isinstance(value, dict):
                return format_str.format(**value)
            else:
                return format_str.format(value)
        else:
            # Just use the template as is
            return template
    
    def generate_choices(self, question, template, count):
        """Generate choices for a question, with randomized correct answer position."""
        if isinstance(template, dict) and 'choices' in template:
            # Get choices from template
            choices_data = template['choices']
            correct_choice_text = choices_data.get('correct', 'True answer')
            incorrect_choices = choices_data.get('incorrect', ['False answer 1', 'False answer 2', 'False answer 3'])
            
            # Make sure we have enough incorrect choices
            while len(incorrect_choices) < count - 1:
                incorrect_choices.append(f"Additional option {len(incorrect_choices) + 1}")
            
            # Randomize the position of the correct answer
            all_choices = [{'text': correct_choice_text, 'is_correct': True}]
            for text in incorrect_choices[:count-1]:
                all_choices.append({'text': text, 'is_correct': False})
            
            random.shuffle(all_choices)
            
            # Create the choices
            for choice_data in all_choices:
                Choice.objects.create(
                    question=question,
                    text=choice_data['text'],
                    is_correct=choice_data['is_correct']
                )
        else:
            # Create generic choices
            correct_position = random.randint(0, count - 1)
            
            for i in range(count):
                is_correct = (i == correct_position)
                choice_text = f"Answer {chr(65 + i)}" + (" (Correct)" if is_correct else "")
                
                Choice.objects.create(
                    question=question,
                    text=choice_text,
                    is_correct=is_correct
                )
    
    def get_question_templates(self, category_name):
        """Get question templates for a specific category."""
        templates = {
            'Science': [
                {
                    'format': "What is the chemical symbol for {}?",
                    'values': ['Oxygen', 'Carbon', 'Hydrogen', 'Nitrogen', 'Calcium'],
                    'choices': {
                        'correct': "The correct chemical symbol",
                        'incorrect': ["Wrong symbol 1", "Wrong symbol 2", "Wrong symbol 3"]
                    }
                },
                {
                    'format': "Who discovered {0}?",
                    'values': ['penicillin', 'gravity', 'the structure of DNA', 'electricity', 'radioactivity'],
                    'choices': {
                        'correct': "The correct discoverer",
                        'incorrect': ["Wrong person 1", "Wrong person 2", "Wrong person 3"]
                    }
                },
                "What is the process called when plants convert light energy to chemical energy?",
                "What is the hardest natural substance on Earth?",
                "Which planet has the most moons in our solar system?",
                "What particles make up an atom?",
                "What is the speed of light in a vacuum?",
                "What is the largest organ in the human body?",
                "What is the most abundant gas in Earth's atmosphere?",
                "What is the process called when water changes from liquid to gas?",
                "How many bones are in the adult human body?",
                "What is the smallest unit of life that can replicate independently?",
                "What causes the northern lights (aurora borealis)?",
                "Which blood type is known as the universal donor?",
                "What type of energy is stored in chemical bonds?"
            ],
            'History': [
                {
                    'format': "In what year did {} occur?",
                    'values': ['World War I begin', 'the American Civil War end', 'the fall of the Berlin Wall', 'the French Revolution begin'],
                    'choices': {
                        'correct': "The correct year",
                        'incorrect': ["Wrong year 1", "Wrong year 2", "Wrong year 3"]
                    }
                },
                "Who was the first Emperor of Rome?",
                "Which ancient civilization built the Machu Picchu complex?",
                "Who wrote the 'I Have a Dream' speech?",
                "Which country was the first to reach the South Pole?",
                "Who was the first woman to win a Nobel Prize?",
                "What was the name of the ship that brought the Pilgrims to America in 1620?",
                "Which treaty ended World War I?",
                "Who was the first President of the United States?",
                "What ancient wonder was located in Alexandria, Egypt?",
                "In which country did the Industrial Revolution begin?",
                "Who painted the Mona Lisa?",
                "What was the name of the conflict between the United States and Great Britain in 1812?",
                "What civilization is credited with creating the first written legal code?",
                "Who was the leader of the Soviet Union during the Cuban Missile Crisis?"
            ],
            'Geography': [
                {
                    'format': "What is the capital of {}?",
                    'values': ['Brazil', 'Australia', 'Canada', 'Japan', 'Egypt', 'Sweden'],
                    'choices': {
                        'correct': "The correct capital",
                        'incorrect': ["Wrong capital 1", "Wrong capital 2", "Wrong capital 3"]
                    }
                },
                "Which is the longest river in the world?",
                "What is the smallest country in the world?",
                "Which desert is the largest in the world?",
                "What is the highest mountain in the world?",
                "Which ocean is the largest?",
                "What is the largest island in the world?",
                "Which country has the most natural lakes?",
                "What is the driest place on Earth?",
                "Which country is both a continent and a country?",
                "What is the capital city of New Zealand?",
                "Which African country has the largest population?",
                "What is the name of the largest coral reef system?",
                "Which mountain range separates Europe and Asia?",
                "What is the lowest point on Earth's surface?"
            ],
            'Technology': [
                {
                    'format': "Who founded {}?",
                    'values': ['Microsoft', 'Apple', 'Amazon', 'Google', 'Facebook'],
                    'choices': {
                        'correct': "The correct founder(s)",
                        'incorrect': ["Wrong person 1", "Wrong person 2", "Wrong person 3"]
                    }
                },
                "What does CPU stand for?",
                "In what year was the first iPhone released?",
                "What programming language was created by Guido van Rossum?",
                "What does HTML stand for?",
                "Which company developed the first commercially successful personal computer?",
                "What is the name of the world's first programmable computer?",
                "Who is credited with inventing the World Wide Web?",
                "What is the term for unwanted emails?",
                "What technology is used to record cryptocurrency transactions?",
                "What was the name of the first web browser?",
                "What does AI stand for in the context of computer science?",
                "What year was the first email sent?",
                "What is the most widely used operating system for smartphones?",
                "What is the name of the virtual assistant developed by Amazon?"
            ]
        }
        
        # Return templates for the category or a default list
        return templates.get(category_name, [
            "Default question 1?",
            "Default question 2?",
            "Default question 3?",
            "Default question 4?",
            "Default question 5?"
        ]) 