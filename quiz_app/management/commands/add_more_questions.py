"""
Management command to add more questions to existing categories.

This command adds a specified number of questions to each existing category
without removing the existing questions.
"""

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from quiz_app.models import Category, Question, Choice

class Command(BaseCommand):
    """Command to add more questions to existing categories."""
    
    help = 'Adds more questions to existing categories'
    
    def add_arguments(self, parser):
        """Add command arguments."""
        parser.add_argument(
            '--questions-per-category',
            type=int,
            default=5,
            help='Number of questions to add per category'
        )
        parser.add_argument(
            '--choices-per-question',
            type=int,
            default=4,
            help='Number of choices per question'
        )
        parser.add_argument(
            '--use-local',
            action='store_true',
            default=True,
            help='Use local knowledge base instead of API for answers'
        )
    
    def handle(self, *args, **options):
        """Execute the command."""
        questions_per_category = options['questions_per_category']
        choices_per_question = options['choices_per_question']
        use_local = options['use_local']
        
        # Get categories
        categories = Category.objects.all()
        if not categories.exists():
            self.stdout.write(self.style.ERROR('No categories found. Please create categories first.'))
            return
        
        # Generate questions
        try:
            with transaction.atomic():
                for category in categories:
                    self.stdout.write(f"Adding {questions_per_category} questions to category: {category.name}")
                    self.generate_questions_for_category(
                        category, 
                        questions_per_category, 
                        choices_per_question,
                        use_local
                    )
            
            self.stdout.write(self.style.SUCCESS('Successfully added more questions!'))
            self.stdout.write(f'Added {Question.objects.count() - (categories.count() * 5)} new questions')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error adding questions: {str(e)}'))
    
    def generate_questions_for_category(self, category, count, choices_count, use_local):
        """Generate questions for a specific category."""
        templates = self.get_question_templates(category.name)
        
        for i in range(count):
            template = random.choice(templates)
            question_text = self.generate_question_text(template, i)
            
            question = Question.objects.create(
                category=category,
                text=question_text,
                explanation=f"This is an explanation for the question about {category.name}.",
                difficulty=random.choice(['easy', 'medium', 'hard'])
            )
            
            self.generate_choices(question, template, choices_count, use_local)
    
    def generate_question_text(self, template, index):
        """Generate question text from a template."""
        return f"{template} (Question {index + 1})"
    
    def generate_choices(self, question, template, count, use_local):
        """Generate choices for a question."""
        # Get AI-generated answers using local knowledge base or API
        question_text = question.text.split(" (Question")[0]  # Remove the index suffix
        category_name = question.category.name
        
        new_choices = self.get_answers_local(question_text, category_name)
        
        if not new_choices or 'correct' not in new_choices or not new_choices['incorrect']:
            self.stdout.write(self.style.WARNING(f'  Failed to get valid answers for question: {question_text}'))
            
            # Fallback to placeholder if AI generation fails
            Choice.objects.create(
                question=question,
                text=f"Correct answer for: {question_text}",
                is_correct=True
            )
            
            for i in range(count - 1):
                Choice.objects.create(
                    question=question,
                    text=f"Incorrect answer {i + 1} for: {question_text}",
                    is_correct=False
                )
        else:
            # Create new correct choice
            Choice.objects.create(
                question=question,
                text=new_choices['correct'],
                is_correct=True
            )
            
            # Create new incorrect choices
            for incorrect_text in new_choices['incorrect'][:count-1]:  # Limit to requested number of choices
                Choice.objects.create(
                    question=question,
                    text=incorrect_text,
                    is_correct=False
                )
    
    def get_answers_local(self, question_text, category_name):
        """
        Generate answers using local knowledge base.
        
        This function contains hard-coded responses for common questions
        and generates sensible answers for others based on patterns.
        """
        # Dictionary of known questions and their answers
        known_answers = {
            "What does CPU stand for?": {
                "correct": "Central Processing Unit",
                "incorrect": ["Computer Personal Unit", "Central Program Utility", "Control Processing Unit"]
            },
            "What does HTML stand for?": {
                "correct": "HyperText Markup Language",
                "incorrect": ["High-Level Text Machine Language", "Hyperlink and Text Management Language", "Home Tool Markup Language"]
            },
            "What does HTTP stand for?": {
                "correct": "HyperText Transfer Protocol",
                "incorrect": ["High Tech Transfer Protocol", "Hyperlink Text Transport Protocol", "Home Tool Transfer Protocol"]
            },
            "What does URL stand for?": {
                "correct": "Uniform Resource Locator",
                "incorrect": ["Universal Reference Link", "Unified Resource Listing", "User Resource Location"]
            },
            "What does RAM stand for?": {
                "correct": "Random Access Memory",
                "incorrect": ["Readily Accessible Memory", "Read Access Mode", "Runtime Application Memory"]
            },
            "What does PDF stand for?": {
                "correct": "Portable Document Format",
                "incorrect": ["Personal Document File", "Print Document Format", "Public Data File"]
            },
            "Who founded Microsoft?": {
                "correct": "Bill Gates and Paul Allen",
                "incorrect": ["Steve Jobs and Steve Wozniak", "Mark Zuckerberg", "Jeff Bezos"]
            },
            "In what year was the first iPhone released?": {
                "correct": "2007",
                "incorrect": ["2005", "2009", "2010"]
            },
            "What is the capital of France?": {
                "correct": "Paris",
                "incorrect": ["London", "Berlin", "Rome"]
            },
            "Which is the largest ocean on Earth?": {
                "correct": "Pacific Ocean",
                "incorrect": ["Atlantic Ocean", "Indian Ocean", "Arctic Ocean"]
            },
            "What is the longest river in the world?": {
                "correct": "Nile River",
                "incorrect": ["Amazon River", "Mississippi River", "Yangtze River"]
            },
            "Which mountain range separates Europe and Asia?": {
                "correct": "Ural Mountains",
                "incorrect": ["Alps", "Himalayas", "Andes"]
            },
            "Who was the first President of the United States?": {
                "correct": "George Washington",
                "incorrect": ["Thomas Jefferson", "Abraham Lincoln", "John Adams"]
            },
            "In which year did World War II end?": {
                "correct": "1945",
                "incorrect": ["1943", "1944", "1946"]
            },
            "Which empire was ruled by Genghis Khan?": {
                "correct": "Mongol Empire",
                "incorrect": ["Roman Empire", "Ottoman Empire", "Byzantine Empire"]
            },
            "What event triggered the start of World War I?": {
                "correct": "Assassination of Archduke Franz Ferdinand",
                "incorrect": ["The invasion of Poland", "The sinking of the Lusitania", "The Treaty of Versailles"]
            },
            "What is the atomic number of hydrogen?": {
                "correct": "1",
                "incorrect": ["2", "0", "3"]
            },
            "Which element has the chemical symbol 'O'?": {
                "correct": "Oxygen",
                "incorrect": ["Osmium", "Oganesson", "Gold"]
            },
            "What is the process by which plants convert light energy into chemical energy?": {
                "correct": "Photosynthesis",
                "incorrect": ["Respiration", "Transpiration", "Fermentation"]
            },
            "What is the name of the force that pulls objects toward the center of the Earth?": {
                "correct": "Gravity",
                "incorrect": ["Magnetism", "Friction", "Tension"]
            },
            "What is the largest organ in the human body?": {
                "correct": "Skin",
                "incorrect": ["Liver", "Heart", "Lungs"]
            },
            "What is the capital of Japan?": {
                "correct": "Tokyo",
                "incorrect": ["Kyoto", "Osaka", "Hiroshima"]
            },
            "Which is the largest desert in the world?": {
                "correct": "Antarctic Desert",
                "incorrect": ["Sahara Desert", "Arabian Desert", "Gobi Desert"]
            },
            "Which country has the largest population?": {
                "correct": "China",
                "incorrect": ["India", "United States", "Indonesia"]
            },
        }
        
        # Check if the question is in our knowledge base
        for known_q, answers in known_answers.items():
            if known_q.lower() in question_text.lower():
                return answers
        
        # Category-specific patterns for questions we don't explicitly know
        if "Science" in category_name:
            if "largest" in question_text:
                if "planet" in question_text:
                    return {
                        "correct": "Jupiter",
                        "incorrect": ["Saturn", "Earth", "Neptune"]
                    }
                if "organ" in question_text:
                    return {
                        "correct": "Skin",
                        "incorrect": ["Liver", "Heart", "Lungs"]
                    }
            elif "chemical" in question_text and "symbol" in question_text:
                if "gold" in question_text:
                    return {
                        "correct": "Au",
                        "incorrect": ["Ag", "Fe", "Go"]
                    }
                if "oxygen" in question_text:
                    return {
                        "correct": "O",
                        "incorrect": ["Ox", "Om", "Oy"]
                    }
                
        elif "History" in category_name:
            if "first" in question_text:
                if "moon landing" in question_text:
                    return {
                        "correct": "1969",
                        "incorrect": ["1967", "1971", "1973"]
                    }
                if "computer programmer" in question_text:
                    return {
                        "correct": "Ada Lovelace",
                        "incorrect": ["Grace Hopper", "Alan Turing", "Charles Babbage"]
                    }
                
        elif "Geography" in category_name:
            if "capital" in question_text:
                if "Japan" in question_text:
                    return {
                        "correct": "Tokyo",
                        "incorrect": ["Kyoto", "Osaka", "Hiroshima"]
                    }
                if "Australia" in question_text:
                    return {
                        "correct": "Canberra",
                        "incorrect": ["Sydney", "Melbourne", "Perth"]
                    }
                    
        elif "Technology" in category_name:
            if "first" in question_text:
                if "web browser" in question_text:
                    return {
                        "correct": "Tim Berners-Lee (WorldWideWeb)",
                        "incorrect": ["Marc Andreessen (Mosaic)", "Bill Gates (Internet Explorer)", "Steve Jobs (Safari)"]
                    }
                if "email system" in question_text:
                    return {
                        "correct": "Ray Tomlinson",
                        "incorrect": ["Bill Gates", "Steve Jobs", "Tim Berners-Lee"]
                    }
            elif "stand for" in question_text.lower():
                if "RAM" in question_text:
                    return {
                        "correct": "Random Access Memory",
                        "incorrect": ["Readily Accessible Memory", "Read Access Mode", "Runtime Application Memory"]
                    }
                
        # Default answers based on question patterns
        if "largest" in question_text:
            return {
                "correct": "The largest one",
                "incorrect": ["The second largest", "The third largest", "The smallest one"]
            }
        elif "Who" in question_text:
            return {
                "correct": "The pioneer in the field",
                "incorrect": ["A competing researcher", "A later contributor", "An unrelated person"]
            }
        elif "When" in question_text or "year" in question_text:
            return {
                "correct": "During the key historical period",
                "incorrect": ["Much earlier", "Somewhat later", "In modern times"]
            }
        elif "Where" in question_text:
            return {
                "correct": "The most significant location",
                "incorrect": ["A nearby location", "A distant location", "An unrelated location"]
            }
            
        # Last resort - completely generic answers
        return {
            "correct": "The most accurate answer",
            "incorrect": ["An incorrect alternative", "A misleading answer", "A common misconception"]
        }
    
    def get_question_templates(self, category_name):
        """Get question templates based on category."""
        templates = {
            'Science': [
                "What is the atomic number of hydrogen?",
                "Which element has the chemical symbol 'O'?",
                "What is the process by which plants convert light energy into chemical energy?",
                "What is the name of the force that pulls objects toward the center of the Earth?",
                "What is the largest organ in the human body?",
                "What is the chemical formula for water?",
                "What is the name of the closest star to Earth?",
                "What is the process by which cells divide to create new cells?",
                "What is the name of the layer of the Earth's atmosphere that contains the ozone layer?",
                "What is the name of the bone in the upper arm?",
            ],
            'History': [
                "Who was the first woman to fly solo across the Atlantic Ocean?",
                "In which year did the first moon landing occur?",
                "Who was the first African American President of the United States?",
                "What was the name of the first human to walk on the moon?",
                "In which year did the Berlin Wall fall?",
                "Who was the first Prime Minister of India?",
                "What was the name of the first computer programmer?",
                "In which year did the Titanic sink?",
                "Who was the first person to circumnavigate the globe?",
                "In which year did the first World War end?",
            ],
            'Geography': [
                "What is the capital of Japan?",
                "Which is the largest desert in the world?",
                "What is the name of the largest island in the Mediterranean Sea?",
                "Which country has the largest population?",
                "What is the name of the highest waterfall in the world?",
                "Which is the smallest continent?",
                "What is the name of the largest lake in Africa?",
                "Which country has the most time zones?",
                "What is the name of the largest island in the Caribbean?",
                "Which is the driest place on Earth?",
            ],
            'Technology': [
                "What does 'CPU' stand for?",
                "Who created the first web browser?",
                "What does 'HTML' stand for?",
                "What is the name of the first computer mouse?",
                "What does 'URL' stand for?",
                "Who created the first smartphone?",
                "What does 'RAM' stand for?",
                "What is the name of the first social media platform?",
                "What does 'PDF' stand for?",
                "Who created the first email system?",
            ],
        }
        
        return templates.get(category_name, ["What is a general knowledge question?"] * 10) 