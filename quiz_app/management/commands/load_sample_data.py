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
                        'explanation': 'Canada has more lakes than any other country, with over 2 million lakes covering about 9% of its territory.',
                        'choices': [
                            {'text': 'United States', 'is_correct': False},
                            {'text': 'Russia', 'is_correct': False},
                            {'text': 'Finland', 'is_correct': False},
                            {'text': 'Canada', 'is_correct': True},
                        ]
                    },
                ]
            },
            {
                'name': 'Technology',
                'description': 'Challenge yourself with questions about computers, software, gadgets, and the digital world.',
                'icon': 'fa-laptop-code',
                'questions': [
                    {
                        'text': 'Who founded Microsoft?',
                        'difficulty': 'easy',
                        'explanation': 'Microsoft was founded by Bill Gates and Paul Allen in 1975.',
                        'choices': [
                            {'text': 'Steve Jobs and Steve Wozniak', 'is_correct': False},
                            {'text': 'Mark Zuckerberg', 'is_correct': False},
                            {'text': 'Bill Gates and Paul Allen', 'is_correct': True},
                            {'text': 'Larry Page and Sergey Brin', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What does "HTTP" stand for?',
                        'difficulty': 'easy',
                        'explanation': 'HTTP stands for Hypertext Transfer Protocol, the foundation of data communication on the World Wide Web.',
                        'choices': [
                            {'text': 'Hypertext Transfer Protocol', 'is_correct': True},
                            {'text': 'Hypertext Technical Processing', 'is_correct': False},
                            {'text': 'High Transfer Text Protocol', 'is_correct': False},
                            {'text': 'Hypertext Terminal Process', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which programming language was created by Guido van Rossum?',
                        'difficulty': 'medium',
                        'explanation': 'Python was created by Guido van Rossum and first released in 1991.',
                        'choices': [
                            {'text': 'Java', 'is_correct': False},
                            {'text': 'Python', 'is_correct': True},
                            {'text': 'C++', 'is_correct': False},
                            {'text': 'Ruby', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the name of the technology that allows devices to connect to the internet without using cables?',
                        'difficulty': 'medium',
                        'explanation': 'Wi-Fi (Wireless Fidelity) is a wireless networking technology that allows devices to connect to the internet without cables.',
                        'choices': [
                            {'text': 'Bluetooth', 'is_correct': False},
                            {'text': 'Ethernet', 'is_correct': False},
                            {'text': 'Wi-Fi', 'is_correct': True},
                            {'text': 'NFC', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What does the acronym "RAID" stand for in computing?',
                        'difficulty': 'hard',
                        'explanation': 'RAID stands for Redundant Array of Independent Disks, a data storage virtualization technology.',
                        'choices': [
                            {'text': 'Random Access Internet Drive', 'is_correct': False},
                            {'text': 'Redundant Array of Independent Disks', 'is_correct': True},
                            {'text': 'Remote Access Input Device', 'is_correct': False},
                            {'text': 'Runtime Application Integration Design', 'is_correct': False},
                        ]
                    },
                ]
            },
        ]
        
        try:
            with transaction.atomic():
                # Clear existing data to avoid duplicates
                self.stdout.write('Clearing existing quiz data...')
                Choice.objects.all().delete()
                Question.objects.all().delete()
                Category.objects.all().delete()
                
                # Create new categories and questions
                for category_data in categories:
                    self.stdout.write(f"Creating category: {category_data['name']}")
                    
                    category = Category.objects.create(
                        name=category_data['name'],
                        description=category_data['description'],
                        icon=category_data['icon']
                    )
                    
                    for question_data in category_data['questions']:
                        self.stdout.write(f"  - Adding question: {question_data['text'][:50]}...")
                        
                        question = Question.objects.create(
                            category=category,
                            text=question_data['text'],
                            explanation=question_data['explanation'],
                            difficulty=question_data['difficulty']
                        )
                        
                        for choice_data in question_data['choices']:
                            Choice.objects.create(
                                question=question,
                                text=choice_data['text'],
                                is_correct=choice_data['is_correct']
                            )
            
            self.stdout.write(self.style.SUCCESS('Successfully loaded sample quiz data!'))
            self.stdout.write(f'Created {Category.objects.count()} categories')
            self.stdout.write(f'Created {Question.objects.count()} questions')
            self.stdout.write(f'Created {Choice.objects.count()} choices')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading sample data: {str(e)}')) 