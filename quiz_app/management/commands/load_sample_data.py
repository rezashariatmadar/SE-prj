"""
Management command to load sample quiz data.

This command creates sample categories and questions to populate the database
for testing and demonstration purposes.
"""

import random
from django.core.management.base import BaseCommand
from django.db import transaction
from quiz_app.models import Category, Question, Choice


class Command(BaseCommand):
    """Command to load sample quiz data into the database."""
    
    help = 'Loads sample quiz categories and questions into the database'
    
    def handle(self, *args, **options):
        """Execute the command to load sample data."""
        self.stdout.write('Loading sample quiz data...')
        
        # Define categories with their descriptions and icons
        categories = [
            {
                'name': 'Science',
                'description': 'Test your knowledge of scientific concepts, discoveries, and famous scientists.',
                'icon': 'fa-flask',
                'questions': [
                    {
                        'text': 'What is the chemical symbol for gold?',
                        'difficulty': 'easy',
                        'explanation': 'Gold\'s chemical symbol Au comes from the Latin word "aurum".',
                        'choices': [
                            {'text': 'Au', 'is_correct': True},
                            {'text': 'Ag', 'is_correct': False},
                            {'text': 'Fe', 'is_correct': False},
                            {'text': 'Go', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which planet is known as the Red Planet?',
                        'difficulty': 'easy',
                        'explanation': 'Mars appears reddish due to iron oxide (rust) on its surface.',
                        'choices': [
                            {'text': 'Venus', 'is_correct': False},
                            {'text': 'Mars', 'is_correct': True},
                            {'text': 'Jupiter', 'is_correct': False},
                            {'text': 'Mercury', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the largest organ in the human body?',
                        'difficulty': 'medium',
                        'explanation': 'The skin is the largest organ by surface area and weight.',
                        'choices': [
                            {'text': 'Liver', 'is_correct': False},
                            {'text': 'Brain', 'is_correct': False},
                            {'text': 'Skin', 'is_correct': True},
                            {'text': 'Intestines', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What causes a rainbow to appear?',
                        'difficulty': 'medium',
                        'explanation': 'Rainbows are caused by the refraction, reflection, and dispersion of light in water droplets.',
                        'choices': [
                            {'text': 'Light refraction through water droplets', 'is_correct': True},
                            {'text': 'Pollution in the atmosphere', 'is_correct': False},
                            {'text': 'Earth\'s magnetic field', 'is_correct': False},
                            {'text': 'Reflection of sunlight on clouds', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the Heisenberg Uncertainty Principle?',
                        'difficulty': 'hard',
                        'explanation': 'The principle states that you cannot simultaneously know the exact position and momentum of a particle.',
                        'choices': [
                            {'text': 'You cannot know both the position and momentum of a particle precisely', 'is_correct': True},
                            {'text': 'The act of observation changes the behavior of particles', 'is_correct': False},
                            {'text': 'All particles exist in multiple states simultaneously', 'is_correct': False},
                            {'text': 'Energy is neither created nor destroyed', 'is_correct': False},
                        ]
                    },
                ]
            },
            {
                'name': 'History',
                'description': 'Explore the events, people, and civilizations that shaped our world.',
                'icon': 'fa-landmark',
                'questions': [
                    {
                        'text': 'Who was the first President of the United States?',
                        'difficulty': 'easy',
                        'explanation': 'George Washington served as the first U.S. President from 1789 to 1797.',
                        'choices': [
                            {'text': 'Thomas Jefferson', 'is_correct': False},
                            {'text': 'George Washington', 'is_correct': True},
                            {'text': 'Abraham Lincoln', 'is_correct': False},
                            {'text': 'John Adams', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did World War II end?',
                        'difficulty': 'easy',
                        'explanation': 'World War II ended in 1945 with the surrender of Japan after the atomic bombings of Hiroshima and Nagasaki.',
                        'choices': [
                            {'text': '1943', 'is_correct': False},
                            {'text': '1944', 'is_correct': False},
                            {'text': '1945', 'is_correct': True},
                            {'text': '1946', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which empire was ruled by Genghis Khan?',
                        'difficulty': 'medium',
                        'explanation': 'Genghis Khan founded and ruled the Mongol Empire, one of the largest empires in history.',
                        'choices': [
                            {'text': 'Roman Empire', 'is_correct': False},
                            {'text': 'Ottoman Empire', 'is_correct': False},
                            {'text': 'Mongol Empire', 'is_correct': True},
                            {'text': 'Byzantine Empire', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What event triggered the start of World War I?',
                        'difficulty': 'medium',
                        'explanation': 'The assassination of Archduke Franz Ferdinand of Austria in Sarajevo in 1914 triggered the chain of events leading to World War I.',
                        'choices': [
                            {'text': 'The invasion of Poland', 'is_correct': False},
                            {'text': 'The sinking of the Lusitania', 'is_correct': False},
                            {'text': 'The assassination of Archduke Franz Ferdinand', 'is_correct': True},
                            {'text': 'The Treaty of Versailles', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which ancient civilization built the Machu Picchu complex in Peru?',
                        'difficulty': 'hard',
                        'explanation': 'Machu Picchu was built by the Inca civilization around 1450 AD.',
                        'choices': [
                            {'text': 'Maya', 'is_correct': False},
                            {'text': 'Aztec', 'is_correct': False},
                            {'text': 'Olmec', 'is_correct': False},
                            {'text': 'Inca', 'is_correct': True},
                        ]
                    },
                ]
            },
            {
                'name': 'Geography',
                'description': 'Test your knowledge of countries, capitals, natural features, and global cultures.',
                'icon': 'fa-globe',
                'questions': [
                    {
                        'text': 'What is the capital of France?',
                        'difficulty': 'easy',
                        'explanation': 'Paris is the capital and most populous city of France.',
                        'choices': [
                            {'text': 'Berlin', 'is_correct': False},
                            {'text': 'London', 'is_correct': False},
                            {'text': 'Paris', 'is_correct': True},
                            {'text': 'Rome', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest ocean on Earth?',
                        'difficulty': 'easy',
                        'explanation': 'The Pacific Ocean is the largest and deepest ocean on Earth, covering more than 30% of the Earth\'s surface.',
                        'choices': [
                            {'text': 'Atlantic Ocean', 'is_correct': False},
                            {'text': 'Indian Ocean', 'is_correct': False},
                            {'text': 'Arctic Ocean', 'is_correct': False},
                            {'text': 'Pacific Ocean', 'is_correct': True},
                        ]
                    },
                    {
                        'text': 'What is the longest river in the world?',
                        'difficulty': 'medium',
                        'explanation': 'The Nile River in Africa is the longest river in the world, stretching about 6,650 kilometers.',
                        'choices': [
                            {'text': 'Amazon River', 'is_correct': False},
                            {'text': 'Nile River', 'is_correct': True},
                            {'text': 'Mississippi River', 'is_correct': False},
                            {'text': 'Yangtze River', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which mountain range separates Europe and Asia?',
                        'difficulty': 'medium',
                        'explanation': 'The Ural Mountains form a natural boundary between Europe and Asia.',
                        'choices': [
                            {'text': 'Alps', 'is_correct': False},
                            {'text': 'Himalayas', 'is_correct': False},
                            {'text': 'Ural Mountains', 'is_correct': True},
                            {'text': 'Andes', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which country has the most natural lakes?',
                        'difficulty': 'hard',
                        'explanation': 'Canada has more natural lakes than any other country, with over 2 million lakes.',
                        'choices': [
                            {'text': 'Russia', 'is_correct': False},
                            {'text': 'United States', 'is_correct': False},
                            {'text': 'Canada', 'is_correct': True},
                            {'text': 'Finland', 'is_correct': False},
                        ]
                    },
                ]
            },
            {
                'name': 'Technology',
                'description': 'Test your knowledge of computers, programming, and modern technology.',
                'icon': 'fa-laptop-code',
                'questions': [
                    {
                        'text': 'What does HTML stand for?',
                        'difficulty': 'easy',
                        'explanation': 'HTML stands for HyperText Markup Language, the standard language for creating web pages.',
                        'choices': [
                            {'text': 'HyperText Markup Language', 'is_correct': True},
                            {'text': 'High Tech Modern Language', 'is_correct': False},
                            {'text': 'Hyper Transfer Markup Language', 'is_correct': False},
                            {'text': 'Home Tool Markup Language', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which programming language is known for its use in data science and machine learning?',
                        'difficulty': 'easy',
                        'explanation': 'Python is widely used in data science and machine learning due to its extensive libraries and frameworks.',
                        'choices': [
                            {'text': 'Java', 'is_correct': False},
                            {'text': 'Python', 'is_correct': True},
                            {'text': 'C++', 'is_correct': False},
                            {'text': 'JavaScript', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the main purpose of a database?',
                        'difficulty': 'medium',
                        'explanation': 'A database is designed to store, organize, and retrieve data efficiently.',
                        'choices': [
                            {'text': 'To store and organize data', 'is_correct': True},
                            {'text': 'To create user interfaces', 'is_correct': False},
                            {'text': 'To process images', 'is_correct': False},
                            {'text': 'To send emails', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of a firewall in computer security?',
                        'difficulty': 'medium',
                        'explanation': 'A firewall monitors and controls incoming and outgoing network traffic based on predetermined security rules.',
                        'choices': [
                            {'text': 'To block unauthorized access', 'is_correct': True},
                            {'text': 'To speed up internet connection', 'is_correct': False},
                            {'text': 'To store backup files', 'is_correct': False},
                            {'text': 'To clean computer viruses', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between HTTP and HTTPS?',
                        'difficulty': 'hard',
                        'explanation': 'HTTPS is the secure version of HTTP, using SSL/TLS encryption to protect data transmission.',
                        'choices': [
                            {'text': 'HTTPS uses encryption for secure communication', 'is_correct': True},
                            {'text': 'HTTPS is faster than HTTP', 'is_correct': False},
                            {'text': 'HTTP is more secure than HTTPS', 'is_correct': False},
                            {'text': 'HTTPS is used only for video streaming', 'is_correct': False},
                        ]
                    },
                ]
            },
            {
                'name': 'Literature',
                'description': 'Test your knowledge of books, authors, and literary works.',
                'icon': 'fa-book',
                'questions': [
                    {
                        'text': 'Who wrote "Romeo and Juliet"?',
                        'difficulty': 'easy',
                        'explanation': 'William Shakespeare wrote the famous tragedy "Romeo and Juliet" in the late 16th century.',
                        'choices': [
                            {'text': 'Charles Dickens', 'is_correct': False},
                            {'text': 'William Shakespeare', 'is_correct': True},
                            {'text': 'Jane Austen', 'is_correct': False},
                            {'text': 'Mark Twain', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which novel begins with the line "It was the best of times, it was the worst of times"?',
                        'difficulty': 'easy',
                        'explanation': 'This famous opening line is from Charles Dickens\' "A Tale of Two Cities".',
                        'choices': [
                            {'text': 'Great Expectations', 'is_correct': False},
                            {'text': 'A Tale of Two Cities', 'is_correct': True},
                            {'text': 'Oliver Twist', 'is_correct': False},
                            {'text': 'David Copperfield', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who wrote "Pride and Prejudice"?',
                        'difficulty': 'medium',
                        'explanation': 'Jane Austen wrote "Pride and Prejudice", one of the most famous romance novels in English literature.',
                        'choices': [
                            {'text': 'Emily Brontë', 'is_correct': False},
                            {'text': 'Jane Austen', 'is_correct': True},
                            {'text': 'Charlotte Brontë', 'is_correct': False},
                            {'text': 'Mary Shelley', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which author created the character Sherlock Holmes?',
                        'difficulty': 'medium',
                        'explanation': 'Sir Arthur Conan Doyle created the famous detective Sherlock Holmes.',
                        'choices': [
                            {'text': 'Agatha Christie', 'is_correct': False},
                            {'text': 'Sir Arthur Conan Doyle', 'is_correct': True},
                            {'text': 'Edgar Allan Poe', 'is_correct': False},
                            {'text': 'Raymond Chandler', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the name of the fictional land in "The Lord of the Rings"?',
                        'difficulty': 'hard',
                        'explanation': 'Middle-earth is the fictional setting of J.R.R. Tolkien\'s "The Lord of the Rings" and other works.',
                        'choices': [
                            {'text': 'Narnia', 'is_correct': False},
                            {'text': 'Westeros', 'is_correct': False},
                            {'text': 'Middle-earth', 'is_correct': True},
                            {'text': 'Hogwarts', 'is_correct': False},
                        ]
                    },
                ]
            }
        ]
        
        with transaction.atomic():
            # Clear existing data
            Category.objects.all().delete()
            Question.objects.all().delete()
            Choice.objects.all().delete()
            
            # Create categories and questions
            for category_data in categories:
                category = Category.objects.create(
                    name=category_data['name'],
                    description=category_data['description'],
                    icon=category_data['icon']
                )
                
                for question_data in category_data['questions']:
                    question = Question.objects.create(
                        text=question_data['text'],
                        difficulty=question_data['difficulty'],
                        explanation=question_data['explanation'],
                        category=category
                    )
                    
                    for choice_data in question_data['choices']:
                        Choice.objects.create(
                            text=choice_data['text'],
                            is_correct=choice_data['is_correct'],
                            question=question
                        )
            
            self.stdout.write(self.style.SUCCESS('Successfully loaded sample quiz data!')) 