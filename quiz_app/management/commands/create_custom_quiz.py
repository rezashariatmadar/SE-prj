"""
Management command to create custom categories and questions.

This command creates specified categories and adds questions to each category.
"""

from django.core.management.base import BaseCommand
from django.db import transaction
from quiz_app.models import Category, Question, Choice

class Command(BaseCommand):
    """Command to create custom categories and questions."""
    
    help = 'Creates custom categories and questions'
    
    def handle(self, *args, **options):
        """Execute the command."""
        # Define categories with their descriptions and icons
        categories_data = [
            {
                'name': 'Programming',
                'description': 'Test your knowledge of programming concepts, languages, and best practices.',
                'icon': 'fa-code',
                'questions': [
                    {
                        'text': 'What is the difference between a list and a tuple in Python?',
                        'difficulty': 'medium',
                        'explanation': 'Lists are mutable (can be changed) while tuples are immutable (cannot be changed).',
                        'choices': [
                            {'text': 'Lists are mutable, tuples are immutable', 'is_correct': True},
                            {'text': 'Tuples are mutable, lists are immutable', 'is_correct': False},
                            {'text': 'Both are mutable', 'is_correct': False},
                            {'text': 'Both are immutable', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What does OOP stand for?',
                        'difficulty': 'easy',
                        'explanation': 'OOP stands for Object-Oriented Programming, a programming paradigm based on objects.',
                        'choices': [
                            {'text': 'Object-Oriented Programming', 'is_correct': True},
                            {'text': 'Object-Oriented Protocol', 'is_correct': False},
                            {'text': 'Object-Oriented Process', 'is_correct': False},
                            {'text': 'Object-Oriented Pattern', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is a constructor in OOP?',
                        'difficulty': 'medium',
                        'explanation': 'A constructor is a special method that initializes a newly created object.',
                        'choices': [
                            {'text': 'A method that initializes a new object', 'is_correct': True},
                            {'text': 'A method that destroys an object', 'is_correct': False},
                            {'text': 'A method that copies an object', 'is_correct': False},
                            {'text': 'A method that compares objects', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of the "git" command?',
                        'difficulty': 'medium',
                        'explanation': 'Git is a distributed version control system for tracking changes in source code.',
                        'choices': [
                            {'text': 'Version control system', 'is_correct': True},
                            {'text': 'Package manager', 'is_correct': False},
                            {'text': 'Text editor', 'is_correct': False},
                            {'text': 'Web server', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between "==" and "===" in JavaScript?',
                        'difficulty': 'hard',
                        'explanation': '"==" compares values with type coercion, while "===" compares both values and types.',
                        'choices': [
                            {'text': '== compares values, === compares values and types', 'is_correct': True},
                            {'text': '== compares types, === compares values', 'is_correct': False},
                            {'text': 'They are identical', 'is_correct': False},
                            {'text': '== is for numbers, === is for strings', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is a REST API?',
                        'difficulty': 'medium',
                        'explanation': 'REST (Representational State Transfer) is an architectural style for designing networked applications.',
                        'choices': [
                            {'text': 'A style of web architecture', 'is_correct': True},
                            {'text': 'A programming language', 'is_correct': False},
                            {'text': 'A database system', 'is_correct': False},
                            {'text': 'A web server', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of Docker?',
                        'difficulty': 'medium',
                        'explanation': 'Docker is a platform for developing, shipping, and running applications in containers.',
                        'choices': [
                            {'text': 'Containerization platform', 'is_correct': True},
                            {'text': 'Database management', 'is_correct': False},
                            {'text': 'Web server', 'is_correct': False},
                            {'text': 'Programming language', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between SQL and NoSQL databases?',
                        'difficulty': 'hard',
                        'explanation': 'SQL databases are relational and structured, while NoSQL databases are non-relational and flexible.',
                        'choices': [
                            {'text': 'SQL is relational, NoSQL is non-relational', 'is_correct': True},
                            {'text': 'SQL is newer than NoSQL', 'is_correct': False},
                            {'text': 'SQL is faster than NoSQL', 'is_correct': False},
                            {'text': 'SQL is for web, NoSQL is for mobile', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of the "npm" command?',
                        'difficulty': 'easy',
                        'explanation': 'npm (Node Package Manager) is a package manager for JavaScript.',
                        'choices': [
                            {'text': 'Package manager for JavaScript', 'is_correct': True},
                            {'text': 'Node.js compiler', 'is_correct': False},
                            {'text': 'JavaScript framework', 'is_correct': False},
                            {'text': 'Web server', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between "let" and "const" in JavaScript?',
                        'difficulty': 'medium',
                        'explanation': '"let" allows reassignment, while "const" creates a read-only reference.',
                        'choices': [
                            {'text': 'let can be reassigned, const cannot', 'is_correct': True},
                            {'text': 'const is faster than let', 'is_correct': False},
                            {'text': 'let is for numbers, const is for strings', 'is_correct': False},
                            {'text': 'They are identical', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of the "pip" command?',
                        'difficulty': 'easy',
                        'explanation': 'pip is a package manager for Python packages.',
                        'choices': [
                            {'text': 'Python package manager', 'is_correct': True},
                            {'text': 'Python interpreter', 'is_correct': False},
                            {'text': 'Python compiler', 'is_correct': False},
                            {'text': 'Python IDE', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between "GET" and "POST" HTTP methods?',
                        'difficulty': 'medium',
                        'explanation': 'GET requests data, POST submits data to be processed.',
                        'choices': [
                            {'text': 'GET retrieves data, POST submits data', 'is_correct': True},
                            {'text': 'GET is faster than POST', 'is_correct': False},
                            {'text': 'POST is newer than GET', 'is_correct': False},
                            {'text': 'They are identical', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of the "virtualenv" command?',
                        'difficulty': 'medium',
                        'explanation': 'virtualenv creates isolated Python environments.',
                        'choices': [
                            {'text': 'Creates isolated Python environments', 'is_correct': True},
                            {'text': 'Installs Python packages', 'is_correct': False},
                            {'text': 'Runs Python scripts', 'is_correct': False},
                            {'text': 'Compiles Python code', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between "public" and "private" in OOP?',
                        'difficulty': 'medium',
                        'explanation': 'Public members are accessible from anywhere, private members are only accessible within the class.',
                        'choices': [
                            {'text': 'Public is accessible anywhere, private only within class', 'is_correct': True},
                            {'text': 'Public is faster than private', 'is_correct': False},
                            {'text': 'Private is newer than public', 'is_correct': False},
                            {'text': 'They are identical', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of the "composer" command?',
                        'difficulty': 'medium',
                        'explanation': 'Composer is a dependency manager for PHP.',
                        'choices': [
                            {'text': 'PHP dependency manager', 'is_correct': True},
                            {'text': 'PHP compiler', 'is_correct': False},
                            {'text': 'PHP web server', 'is_correct': False},
                            {'text': 'PHP IDE', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between "var" and "let" in JavaScript?',
                        'difficulty': 'hard',
                        'explanation': '"var" is function-scoped, while "let" is block-scoped.',
                        'choices': [
                            {'text': 'var is function-scoped, let is block-scoped', 'is_correct': True},
                            {'text': 'let is faster than var', 'is_correct': False},
                            {'text': 'var is newer than let', 'is_correct': False},
                            {'text': 'They are identical', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of the "docker-compose" command?',
                        'difficulty': 'hard',
                        'explanation': 'docker-compose is a tool for defining and running multi-container Docker applications.',
                        'choices': [
                            {'text': 'Manages multiple Docker containers', 'is_correct': True},
                            {'text': 'Builds Docker images', 'is_correct': False},
                            {'text': 'Runs Docker containers', 'is_correct': False},
                            {'text': 'Deletes Docker containers', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between "innerHTML" and "textContent"?',
                        'difficulty': 'medium',
                        'explanation': 'innerHTML parses HTML, textContent treats content as plain text.',
                        'choices': [
                            {'text': 'innerHTML parses HTML, textContent is plain text', 'is_correct': True},
                            {'text': 'textContent is faster than innerHTML', 'is_correct': False},
                            {'text': 'innerHTML is newer than textContent', 'is_correct': False},
                            {'text': 'They are identical', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the purpose of the "git merge" command?',
                        'difficulty': 'medium',
                        'explanation': 'git merge combines changes from different branches.',
                        'choices': [
                            {'text': 'Combines changes from different branches', 'is_correct': True},
                            {'text': 'Creates a new branch', 'is_correct': False},
                            {'text': 'Deletes a branch', 'is_correct': False},
                            {'text': 'Renames a branch', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the difference between "async" and "await"?',
                        'difficulty': 'hard',
                        'explanation': 'async declares an asynchronous function, await pauses execution until a Promise resolves.',
                        'choices': [
                            {'text': 'async declares function, await pauses execution', 'is_correct': True},
                            {'text': 'await is faster than async', 'is_correct': False},
                            {'text': 'async is newer than await', 'is_correct': False},
                            {'text': 'They are identical', 'is_correct': False},
                        ]
                    }
                ]
            },
            {
                'name': 'Mathematics',
                'description': 'Challenge yourself with mathematical concepts, formulas, and problem-solving.',
                'icon': 'fa-calculator',
                'questions': [
                    {
                        'text': 'What is the value of π (pi) to two decimal places?',
                        'difficulty': 'easy',
                        'explanation': 'π is approximately 3.14, which is the ratio of a circle\'s circumference to its diameter.',
                        'choices': [
                            {'text': '3.14', 'is_correct': True},
                            {'text': '3.16', 'is_correct': False},
                            {'text': '3.12', 'is_correct': False},
                            {'text': '3.18', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the derivative of x²?',
                        'difficulty': 'medium',
                        'explanation': 'The derivative of x² is 2x, using the power rule of differentiation.',
                        'choices': [
                            {'text': '2x', 'is_correct': True},
                            {'text': 'x²', 'is_correct': False},
                            {'text': '2', 'is_correct': False},
                            {'text': 'x', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the sum of angles in a triangle?',
                        'difficulty': 'easy',
                        'explanation': 'The sum of angles in a triangle is always 180 degrees.',
                        'choices': [
                            {'text': '180 degrees', 'is_correct': True},
                            {'text': '90 degrees', 'is_correct': False},
                            {'text': '360 degrees', 'is_correct': False},
                            {'text': '270 degrees', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the formula for the area of a circle?',
                        'difficulty': 'medium',
                        'explanation': 'The area of a circle is πr², where r is the radius.',
                        'choices': [
                            {'text': 'πr²', 'is_correct': True},
                            {'text': '2πr', 'is_correct': False},
                            {'text': 'πd', 'is_correct': False},
                            {'text': '2πd', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the value of e (Euler\'s number) to two decimal places?',
                        'difficulty': 'medium',
                        'explanation': 'e is approximately 2.72, which is the base of the natural logarithm.',
                        'choices': [
                            {'text': '2.72', 'is_correct': True},
                            {'text': '2.71', 'is_correct': False},
                            {'text': '2.73', 'is_correct': False},
                            {'text': '2.70', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the integral of 2x?',
                        'difficulty': 'hard',
                        'explanation': 'The integral of 2x is x² + C, where C is the constant of integration.',
                        'choices': [
                            {'text': 'x² + C', 'is_correct': True},
                            {'text': '2x² + C', 'is_correct': False},
                            {'text': 'x²', 'is_correct': False},
                            {'text': '2x²', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the Pythagorean theorem?',
                        'difficulty': 'medium',
                        'explanation': 'In a right triangle, a² + b² = c², where c is the hypotenuse.',
                        'choices': [
                            {'text': 'a² + b² = c²', 'is_correct': True},
                            {'text': 'a + b = c', 'is_correct': False},
                            {'text': 'a² - b² = c²', 'is_correct': False},
                            {'text': 'a × b = c', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the value of sin(30°)?',
                        'difficulty': 'medium',
                        'explanation': 'sin(30°) = 0.5, which is a common trigonometric value.',
                        'choices': [
                            {'text': '0.5', 'is_correct': True},
                            {'text': '0.866', 'is_correct': False},
                            {'text': '0.707', 'is_correct': False},
                            {'text': '0.577', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the formula for the volume of a sphere?',
                        'difficulty': 'medium',
                        'explanation': 'The volume of a sphere is (4/3)πr³, where r is the radius.',
                        'choices': [
                            {'text': '(4/3)πr³', 'is_correct': True},
                            {'text': '4πr²', 'is_correct': False},
                            {'text': 'πr³', 'is_correct': False},
                            {'text': '2πr³', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the value of log₁₀(100)?',
                        'difficulty': 'medium',
                        'explanation': 'log₁₀(100) = 2, because 10² = 100.',
                        'choices': [
                            {'text': '2', 'is_correct': True},
                            {'text': '1', 'is_correct': False},
                            {'text': '3', 'is_correct': False},
                            {'text': '0', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the derivative of sin(x)?',
                        'difficulty': 'hard',
                        'explanation': 'The derivative of sin(x) is cos(x).',
                        'choices': [
                            {'text': 'cos(x)', 'is_correct': True},
                            {'text': '-sin(x)', 'is_correct': False},
                            {'text': '-cos(x)', 'is_correct': False},
                            {'text': 'sin(x)', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the sum of the first n natural numbers?',
                        'difficulty': 'hard',
                        'explanation': 'The sum of the first n natural numbers is n(n+1)/2.',
                        'choices': [
                            {'text': 'n(n+1)/2', 'is_correct': True},
                            {'text': 'n²', 'is_correct': False},
                            {'text': 'n(n-1)/2', 'is_correct': False},
                            {'text': 'n²/2', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the value of cos(60°)?',
                        'difficulty': 'medium',
                        'explanation': 'cos(60°) = 0.5, which is a common trigonometric value.',
                        'choices': [
                            {'text': '0.5', 'is_correct': True},
                            {'text': '0.866', 'is_correct': False},
                            {'text': '0.707', 'is_correct': False},
                            {'text': '0.577', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the formula for the area of a triangle?',
                        'difficulty': 'easy',
                        'explanation': 'The area of a triangle is (base × height)/2.',
                        'choices': [
                            {'text': '(base × height)/2', 'is_correct': True},
                            {'text': 'base × height', 'is_correct': False},
                            {'text': 'base + height', 'is_correct': False},
                            {'text': 'base² × height', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the value of tan(45°)?',
                        'difficulty': 'medium',
                        'explanation': 'tan(45°) = 1, which is a common trigonometric value.',
                        'choices': [
                            {'text': '1', 'is_correct': True},
                            {'text': '0.5', 'is_correct': False},
                            {'text': '0.866', 'is_correct': False},
                            {'text': '0.707', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the formula for the perimeter of a rectangle?',
                        'difficulty': 'easy',
                        'explanation': 'The perimeter of a rectangle is 2(length + width).',
                        'choices': [
                            {'text': '2(length + width)', 'is_correct': True},
                            {'text': 'length × width', 'is_correct': False},
                            {'text': 'length + width', 'is_correct': False},
                            {'text': '2(length × width)', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the value of √2 to two decimal places?',
                        'difficulty': 'medium',
                        'explanation': '√2 is approximately 1.41, which is an irrational number.',
                        'choices': [
                            {'text': '1.41', 'is_correct': True},
                            {'text': '1.42', 'is_correct': False},
                            {'text': '1.40', 'is_correct': False},
                            {'text': '1.43', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the formula for the volume of a cylinder?',
                        'difficulty': 'medium',
                        'explanation': 'The volume of a cylinder is πr²h, where r is the radius and h is the height.',
                        'choices': [
                            {'text': 'πr²h', 'is_correct': True},
                            {'text': '2πrh', 'is_correct': False},
                            {'text': 'πrh', 'is_correct': False},
                            {'text': '2πr²h', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the value of log₂(8)?',
                        'difficulty': 'medium',
                        'explanation': 'log₂(8) = 3, because 2³ = 8.',
                        'choices': [
                            {'text': '3', 'is_correct': True},
                            {'text': '2', 'is_correct': False},
                            {'text': '4', 'is_correct': False},
                            {'text': '1', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the derivative of e^x?',
                        'difficulty': 'hard',
                        'explanation': 'The derivative of e^x is e^x.',
                        'choices': [
                            {'text': 'e^x', 'is_correct': True},
                            {'text': 'xe^x', 'is_correct': False},
                            {'text': 'e^(x-1)', 'is_correct': False},
                            {'text': 'xe^(x-1)', 'is_correct': False},
                        ]
                    }
                ]
            },
            {
                'name': 'History',
                'description': 'Explore historical events, figures, and civilizations.',
                'icon': 'fa-landmark',
                'questions': [
                    {
                        'text': 'In which year did World War II end?',
                        'difficulty': 'easy',
                        'explanation': 'World War II ended in 1945 with the surrender of Germany in May and Japan in September.',
                        'choices': [
                            {'text': '1945', 'is_correct': True},
                            {'text': '1944', 'is_correct': False},
                            {'text': '1946', 'is_correct': False},
                            {'text': '1943', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first President of the United States?',
                        'difficulty': 'easy',
                        'explanation': 'George Washington served as the first President of the United States from 1789 to 1797.',
                        'choices': [
                            {'text': 'George Washington', 'is_correct': True},
                            {'text': 'Thomas Jefferson', 'is_correct': False},
                            {'text': 'John Adams', 'is_correct': False},
                            {'text': 'Benjamin Franklin', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the Titanic sink?',
                        'difficulty': 'easy',
                        'explanation': 'The RMS Titanic sank on April 15, 1912, after hitting an iceberg.',
                        'choices': [
                            {'text': '1912', 'is_correct': True},
                            {'text': '1911', 'is_correct': False},
                            {'text': '1913', 'is_correct': False},
                            {'text': '1914', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who wrote the Declaration of Independence?',
                        'difficulty': 'medium',
                        'explanation': 'Thomas Jefferson was the primary author of the Declaration of Independence.',
                        'choices': [
                            {'text': 'Thomas Jefferson', 'is_correct': True},
                            {'text': 'George Washington', 'is_correct': False},
                            {'text': 'John Adams', 'is_correct': False},
                            {'text': 'Benjamin Franklin', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the American Civil War begin?',
                        'difficulty': 'medium',
                        'explanation': 'The American Civil War began in 1861 with the attack on Fort Sumter.',
                        'choices': [
                            {'text': '1861', 'is_correct': True},
                            {'text': '1860', 'is_correct': False},
                            {'text': '1862', 'is_correct': False},
                            {'text': '1863', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first Emperor of Rome?',
                        'difficulty': 'medium',
                        'explanation': 'Augustus (Octavian) was the first Roman Emperor, ruling from 27 BC to 14 AD.',
                        'choices': [
                            {'text': 'Augustus', 'is_correct': True},
                            {'text': 'Julius Caesar', 'is_correct': False},
                            {'text': 'Nero', 'is_correct': False},
                            {'text': 'Constantine', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the French Revolution begin?',
                        'difficulty': 'medium',
                        'explanation': 'The French Revolution began in 1789 with the storming of the Bastille.',
                        'choices': [
                            {'text': '1789', 'is_correct': True},
                            {'text': '1788', 'is_correct': False},
                            {'text': '1790', 'is_correct': False},
                            {'text': '1791', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first female Prime Minister of the United Kingdom?',
                        'difficulty': 'medium',
                        'explanation': 'Margaret Thatcher served as the first female Prime Minister of the UK from 1979 to 1990.',
                        'choices': [
                            {'text': 'Margaret Thatcher', 'is_correct': True},
                            {'text': 'Queen Elizabeth II', 'is_correct': False},
                            {'text': 'Theresa May', 'is_correct': False},
                            {'text': 'Queen Victoria', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the Berlin Wall fall?',
                        'difficulty': 'medium',
                        'explanation': 'The Berlin Wall fell on November 9, 1989, marking the end of the Cold War era.',
                        'choices': [
                            {'text': '1989', 'is_correct': True},
                            {'text': '1988', 'is_correct': False},
                            {'text': '1990', 'is_correct': False},
                            {'text': '1991', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first President of the Russian Federation?',
                        'difficulty': 'medium',
                        'explanation': 'Boris Yeltsin served as the first President of the Russian Federation from 1991 to 1999.',
                        'choices': [
                            {'text': 'Boris Yeltsin', 'is_correct': True},
                            {'text': 'Vladimir Putin', 'is_correct': False},
                            {'text': 'Mikhail Gorbachev', 'is_correct': False},
                            {'text': 'Joseph Stalin', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the United States declare independence?',
                        'difficulty': 'easy',
                        'explanation': 'The United States declared independence on July 4, 1776.',
                        'choices': [
                            {'text': '1776', 'is_correct': True},
                            {'text': '1775', 'is_correct': False},
                            {'text': '1777', 'is_correct': False},
                            {'text': '1778', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first female to win a Nobel Prize?',
                        'difficulty': 'hard',
                        'explanation': 'Marie Curie was the first woman to win a Nobel Prize, receiving it in Physics in 1903.',
                        'choices': [
                            {'text': 'Marie Curie', 'is_correct': True},
                            {'text': 'Rosalind Franklin', 'is_correct': False},
                            {'text': 'Jane Goodall', 'is_correct': False},
                            {'text': 'Florence Nightingale', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the first moon landing occur?',
                        'difficulty': 'medium',
                        'explanation': 'The first moon landing occurred on July 20, 1969, with Apollo 11.',
                        'choices': [
                            {'text': '1969', 'is_correct': True},
                            {'text': '1968', 'is_correct': False},
                            {'text': '1970', 'is_correct': False},
                            {'text': '1971', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first Emperor of China?',
                        'difficulty': 'hard',
                        'explanation': 'Qin Shi Huang was the first Emperor of China, unifying the country in 221 BC.',
                        'choices': [
                            {'text': 'Qin Shi Huang', 'is_correct': True},
                            {'text': 'Confucius', 'is_correct': False},
                            {'text': 'Sun Tzu', 'is_correct': False},
                            {'text': 'Lao Tzu', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the Renaissance begin?',
                        'difficulty': 'hard',
                        'explanation': 'The Renaissance began in Italy in the 14th century, around 1300.',
                        'choices': [
                            {'text': '1300s', 'is_correct': True},
                            {'text': '1200s', 'is_correct': False},
                            {'text': '1400s', 'is_correct': False},
                            {'text': '1500s', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first female to win an Olympic gold medal?',
                        'difficulty': 'hard',
                        'explanation': 'Charlotte Cooper was the first female Olympic champion, winning in tennis in 1900.',
                        'choices': [
                            {'text': 'Charlotte Cooper', 'is_correct': True},
                            {'text': 'Wilma Rudolph', 'is_correct': False},
                            {'text': 'Babe Didrikson', 'is_correct': False},
                            {'text': 'Fanny Blankers-Koen', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the Industrial Revolution begin?',
                        'difficulty': 'hard',
                        'explanation': 'The Industrial Revolution began in Britain in the late 18th century, around 1760.',
                        'choices': [
                            {'text': '1760s', 'is_correct': True},
                            {'text': '1750s', 'is_correct': False},
                            {'text': '1770s', 'is_correct': False},
                            {'text': '1780s', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first female to win a Nobel Prize in Literature?',
                        'difficulty': 'hard',
                        'explanation': 'Selma Lagerlöf was the first woman to win the Nobel Prize in Literature in 1909.',
                        'choices': [
                            {'text': 'Selma Lagerlöf', 'is_correct': True},
                            {'text': 'Pearl S. Buck', 'is_correct': False},
                            {'text': 'Gabriela Mistral', 'is_correct': False},
                            {'text': 'Toni Morrison', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'In which year did the first World War begin?',
                        'difficulty': 'medium',
                        'explanation': 'World War I began in 1914 after the assassination of Archduke Franz Ferdinand.',
                        'choices': [
                            {'text': '1914', 'is_correct': True},
                            {'text': '1913', 'is_correct': False},
                            {'text': '1915', 'is_correct': False},
                            {'text': '1916', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Who was the first female to win a Nobel Prize in Peace?',
                        'difficulty': 'hard',
                        'explanation': 'Baroness Bertha von Suttner was the first woman to win the Nobel Peace Prize in 1905.',
                        'choices': [
                            {'text': 'Baroness Bertha von Suttner', 'is_correct': True},
                            {'text': 'Mother Teresa', 'is_correct': False},
                            {'text': 'Jane Addams', 'is_correct': False},
                            {'text': 'Emily Greene Balch', 'is_correct': False},
                        ]
                    }
                ]
            },
            {
                'name': 'Science',
                'description': 'Test your knowledge of scientific principles, discoveries, and natural phenomena.',
                'icon': 'fa-flask',
                'questions': [
                    {
                        'text': 'What is the chemical symbol for gold?',
                        'difficulty': 'easy',
                        'explanation': 'Au is the chemical symbol for gold, derived from the Latin word "aurum".',
                        'choices': [
                            {'text': 'Au', 'is_correct': True},
                            {'text': 'Ag', 'is_correct': False},
                            {'text': 'Fe', 'is_correct': False},
                            {'text': 'Cu', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process by which plants convert light energy into chemical energy?',
                        'difficulty': 'medium',
                        'explanation': 'Photosynthesis is the process by which plants convert light energy into chemical energy.',
                        'choices': [
                            {'text': 'Photosynthesis', 'is_correct': True},
                            {'text': 'Respiration', 'is_correct': False},
                            {'text': 'Fermentation', 'is_correct': False},
                            {'text': 'Digestion', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the atomic number of carbon?',
                        'difficulty': 'easy',
                        'explanation': 'Carbon has an atomic number of 6, meaning it has 6 protons in its nucleus.',
                        'choices': [
                            {'text': '6', 'is_correct': True},
                            {'text': '12', 'is_correct': False},
                            {'text': '14', 'is_correct': False},
                            {'text': '8', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the speed of light in a vacuum?',
                        'difficulty': 'medium',
                        'explanation': 'The speed of light in a vacuum is approximately 299,792,458 meters per second.',
                        'choices': [
                            {'text': '299,792,458 m/s', 'is_correct': True},
                            {'text': '299,792,458 km/s', 'is_correct': False},
                            {'text': '299,792,458 mi/s', 'is_correct': False},
                            {'text': '299,792,458 ft/s', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the largest organ in the human body?',
                        'difficulty': 'easy',
                        'explanation': 'The skin is the largest organ in the human body, covering the entire body surface.',
                        'choices': [
                            {'text': 'Skin', 'is_correct': True},
                            {'text': 'Liver', 'is_correct': False},
                            {'text': 'Heart', 'is_correct': False},
                            {'text': 'Brain', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical formula for water?',
                        'difficulty': 'easy',
                        'explanation': 'H₂O is the chemical formula for water, consisting of two hydrogen atoms and one oxygen atom.',
                        'choices': [
                            {'text': 'H₂O', 'is_correct': True},
                            {'text': 'CO₂', 'is_correct': False},
                            {'text': 'O₂', 'is_correct': False},
                            {'text': 'H₂', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process of cell division called?',
                        'difficulty': 'medium',
                        'explanation': 'Mitosis is the process of cell division that results in two identical daughter cells.',
                        'choices': [
                            {'text': 'Mitosis', 'is_correct': True},
                            {'text': 'Meiosis', 'is_correct': False},
                            {'text': 'Fission', 'is_correct': False},
                            {'text': 'Fusion', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical symbol for iron?',
                        'difficulty': 'easy',
                        'explanation': 'Fe is the chemical symbol for iron, derived from the Latin word "ferrum".',
                        'choices': [
                            {'text': 'Fe', 'is_correct': True},
                            {'text': 'Ir', 'is_correct': False},
                            {'text': 'In', 'is_correct': False},
                            {'text': 'Fi', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process of converting sugar into alcohol called?',
                        'difficulty': 'medium',
                        'explanation': 'Fermentation is the process of converting sugar into alcohol and carbon dioxide.',
                        'choices': [
                            {'text': 'Fermentation', 'is_correct': True},
                            {'text': 'Distillation', 'is_correct': False},
                            {'text': 'Evaporation', 'is_correct': False},
                            {'text': 'Condensation', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical symbol for silver?',
                        'difficulty': 'easy',
                        'explanation': 'Ag is the chemical symbol for silver, derived from the Latin word "argentum".',
                        'choices': [
                            {'text': 'Ag', 'is_correct': True},
                            {'text': 'Si', 'is_correct': False},
                            {'text': 'Sr', 'is_correct': False},
                            {'text': 'Au', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process of water changing from liquid to gas called?',
                        'difficulty': 'easy',
                        'explanation': 'Evaporation is the process of water changing from liquid to gas state.',
                        'choices': [
                            {'text': 'Evaporation', 'is_correct': True},
                            {'text': 'Condensation', 'is_correct': False},
                            {'text': 'Precipitation', 'is_correct': False},
                            {'text': 'Sublimation', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical symbol for copper?',
                        'difficulty': 'easy',
                        'explanation': 'Cu is the chemical symbol for copper, derived from the Latin word "cuprum".',
                        'choices': [
                            {'text': 'Cu', 'is_correct': True},
                            {'text': 'Co', 'is_correct': False},
                            {'text': 'Cr', 'is_correct': False},
                            {'text': 'Ca', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process of plants releasing water vapor called?',
                        'difficulty': 'medium',
                        'explanation': 'Transpiration is the process of plants releasing water vapor through their leaves.',
                        'choices': [
                            {'text': 'Transpiration', 'is_correct': True},
                            {'text': 'Evaporation', 'is_correct': False},
                            {'text': 'Condensation', 'is_correct': False},
                            {'text': 'Precipitation', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical symbol for lead?',
                        'difficulty': 'medium',
                        'explanation': 'Pb is the chemical symbol for lead, derived from the Latin word "plumbum".',
                        'choices': [
                            {'text': 'Pb', 'is_correct': True},
                            {'text': 'Ld', 'is_correct': False},
                            {'text': 'Le', 'is_correct': False},
                            {'text': 'Pl', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process of converting light energy into electrical energy called?',
                        'difficulty': 'hard',
                        'explanation': 'Photovoltaic effect is the process of converting light energy into electrical energy.',
                        'choices': [
                            {'text': 'Photovoltaic effect', 'is_correct': True},
                            {'text': 'Photosynthesis', 'is_correct': False},
                            {'text': 'Photoelectric effect', 'is_correct': False},
                            {'text': 'Photolysis', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical symbol for mercury?',
                        'difficulty': 'medium',
                        'explanation': 'Hg is the chemical symbol for mercury, derived from the Latin word "hydrargyrum".',
                        'choices': [
                            {'text': 'Hg', 'is_correct': True},
                            {'text': 'Me', 'is_correct': False},
                            {'text': 'Mr', 'is_correct': False},
                            {'text': 'My', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process of converting electrical energy into light energy called?',
                        'difficulty': 'hard',
                        'explanation': 'Electroluminescence is the process of converting electrical energy into light energy.',
                        'choices': [
                            {'text': 'Electroluminescence', 'is_correct': True},
                            {'text': 'Photoluminescence', 'is_correct': False},
                            {'text': 'Chemiluminescence', 'is_correct': False},
                            {'text': 'Bioluminescence', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical symbol for tin?',
                        'difficulty': 'medium',
                        'explanation': 'Sn is the chemical symbol for tin, derived from the Latin word "stannum".',
                        'choices': [
                            {'text': 'Sn', 'is_correct': True},
                            {'text': 'Ti', 'is_correct': False},
                            {'text': 'Tn', 'is_correct': False},
                            {'text': 'St', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the process of converting chemical energy into electrical energy called?',
                        'difficulty': 'hard',
                        'explanation': 'Electrochemistry is the process of converting chemical energy into electrical energy.',
                        'choices': [
                            {'text': 'Electrochemistry', 'is_correct': True},
                            {'text': 'Photochemistry', 'is_correct': False},
                            {'text': 'Thermochemistry', 'is_correct': False},
                            {'text': 'Biochemistry', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the chemical symbol for tungsten?',
                        'difficulty': 'hard',
                        'explanation': 'W is the chemical symbol for tungsten, derived from the German word "Wolfram".',
                        'choices': [
                            {'text': 'W', 'is_correct': True},
                            {'text': 'Tu', 'is_correct': False},
                            {'text': 'Tg', 'is_correct': False},
                            {'text': 'Tw', 'is_correct': False},
                        ]
                    }
                ]
            },
            {
                'name': 'Geography',
                'description': 'Explore countries, capitals, landmarks, and geographical features.',
                'icon': 'fa-globe',
                'questions': [
                    {
                        'text': 'What is the capital of Japan?',
                        'difficulty': 'easy',
                        'explanation': 'Tokyo is the capital and largest city of Japan.',
                        'choices': [
                            {'text': 'Tokyo', 'is_correct': True},
                            {'text': 'Kyoto', 'is_correct': False},
                            {'text': 'Osaka', 'is_correct': False},
                            {'text': 'Nagoya', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest ocean on Earth?',
                        'difficulty': 'easy',
                        'explanation': 'The Pacific Ocean is the largest and deepest ocean on Earth.',
                        'choices': [
                            {'text': 'Pacific Ocean', 'is_correct': True},
                            {'text': 'Atlantic Ocean', 'is_correct': False},
                            {'text': 'Indian Ocean', 'is_correct': False},
                            {'text': 'Arctic Ocean', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of Australia?',
                        'difficulty': 'medium',
                        'explanation': 'Canberra is the capital city of Australia, while Sydney is the largest city.',
                        'choices': [
                            {'text': 'Canberra', 'is_correct': True},
                            {'text': 'Sydney', 'is_correct': False},
                            {'text': 'Melbourne', 'is_correct': False},
                            {'text': 'Brisbane', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the longest river in the world?',
                        'difficulty': 'medium',
                        'explanation': 'The Nile River is the longest river in the world, flowing through northeastern Africa.',
                        'choices': [
                            {'text': 'Nile River', 'is_correct': True},
                            {'text': 'Amazon River', 'is_correct': False},
                            {'text': 'Yangtze River', 'is_correct': False},
                            {'text': 'Mississippi River', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of Brazil?',
                        'difficulty': 'medium',
                        'explanation': 'Brasília is the capital of Brazil, while São Paulo is the largest city.',
                        'choices': [
                            {'text': 'Brasília', 'is_correct': True},
                            {'text': 'São Paulo', 'is_correct': False},
                            {'text': 'Rio de Janeiro', 'is_correct': False},
                            {'text': 'Salvador', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the highest mountain in the world?',
                        'difficulty': 'easy',
                        'explanation': 'Mount Everest is the highest mountain above sea level, at 29,029 feet (8,848 meters).',
                        'choices': [
                            {'text': 'Mount Everest', 'is_correct': True},
                            {'text': 'K2', 'is_correct': False},
                            {'text': 'Kangchenjunga', 'is_correct': False},
                            {'text': 'Lhotse', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of South Africa?',
                        'difficulty': 'hard',
                        'explanation': 'South Africa has three capital cities: Pretoria (executive), Cape Town (legislative), and Bloemfontein (judicial).',
                        'choices': [
                            {'text': 'Pretoria, Cape Town, and Bloemfontein', 'is_correct': True},
                            {'text': 'Johannesburg', 'is_correct': False},
                            {'text': 'Durban', 'is_correct': False},
                            {'text': 'Port Elizabeth', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest desert in the world?',
                        'difficulty': 'medium',
                        'explanation': 'The Antarctic Desert is the largest desert in the world, followed by the Arctic Desert.',
                        'choices': [
                            {'text': 'Antarctic Desert', 'is_correct': True},
                            {'text': 'Sahara Desert', 'is_correct': False},
                            {'text': 'Gobi Desert', 'is_correct': False},
                            {'text': 'Arabian Desert', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of Canada?',
                        'difficulty': 'medium',
                        'explanation': 'Ottawa is the capital of Canada, while Toronto is the largest city.',
                        'choices': [
                            {'text': 'Ottawa', 'is_correct': True},
                            {'text': 'Toronto', 'is_correct': False},
                            {'text': 'Montreal', 'is_correct': False},
                            {'text': 'Vancouver', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest lake in the world?',
                        'difficulty': 'medium',
                        'explanation': 'The Caspian Sea is the largest lake in the world by surface area.',
                        'choices': [
                            {'text': 'Caspian Sea', 'is_correct': True},
                            {'text': 'Lake Superior', 'is_correct': False},
                            {'text': 'Lake Victoria', 'is_correct': False},
                            {'text': 'Lake Baikal', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of India?',
                        'difficulty': 'medium',
                        'explanation': 'New Delhi is the capital of India, while Mumbai is the largest city.',
                        'choices': [
                            {'text': 'New Delhi', 'is_correct': True},
                            {'text': 'Mumbai', 'is_correct': False},
                            {'text': 'Kolkata', 'is_correct': False},
                            {'text': 'Chennai', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest island in the world?',
                        'difficulty': 'medium',
                        'explanation': 'Greenland is the largest island in the world, followed by New Guinea.',
                        'choices': [
                            {'text': 'Greenland', 'is_correct': True},
                            {'text': 'Australia', 'is_correct': False},
                            {'text': 'New Guinea', 'is_correct': False},
                            {'text': 'Borneo', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of China?',
                        'difficulty': 'medium',
                        'explanation': 'Beijing is the capital of China, while Shanghai is the largest city.',
                        'choices': [
                            {'text': 'Beijing', 'is_correct': True},
                            {'text': 'Shanghai', 'is_correct': False},
                            {'text': 'Guangzhou', 'is_correct': False},
                            {'text': 'Shenzhen', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest country in South America?',
                        'difficulty': 'medium',
                        'explanation': 'Brazil is the largest country in South America by both area and population.',
                        'choices': [
                            {'text': 'Brazil', 'is_correct': True},
                            {'text': 'Argentina', 'is_correct': False},
                            {'text': 'Peru', 'is_correct': False},
                            {'text': 'Colombia', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of Russia?',
                        'difficulty': 'medium',
                        'explanation': 'Moscow is the capital of Russia, while Saint Petersburg is the second-largest city.',
                        'choices': [
                            {'text': 'Moscow', 'is_correct': True},
                            {'text': 'Saint Petersburg', 'is_correct': False},
                            {'text': 'Novosibirsk', 'is_correct': False},
                            {'text': 'Yekaterinburg', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest country in Africa?',
                        'difficulty': 'medium',
                        'explanation': 'Algeria is the largest country in Africa by area.',
                        'choices': [
                            {'text': 'Algeria', 'is_correct': True},
                            {'text': 'Democratic Republic of the Congo', 'is_correct': False},
                            {'text': 'Sudan', 'is_correct': False},
                            {'text': 'Libya', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of Egypt?',
                        'difficulty': 'medium',
                        'explanation': 'Cairo is the capital of Egypt and the largest city in Africa.',
                        'choices': [
                            {'text': 'Cairo', 'is_correct': True},
                            {'text': 'Alexandria', 'is_correct': False},
                            {'text': 'Giza', 'is_correct': False},
                            {'text': 'Luxor', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest country in Europe?',
                        'difficulty': 'medium',
                        'explanation': 'Ukraine is the largest country entirely in Europe by area.',
                        'choices': [
                            {'text': 'Ukraine', 'is_correct': True},
                            {'text': 'France', 'is_correct': False},
                            {'text': 'Spain', 'is_correct': False},
                            {'text': 'Germany', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'What is the capital of Mexico?',
                        'difficulty': 'medium',
                        'explanation': 'Mexico City is the capital of Mexico and the largest city in North America.',
                        'choices': [
                            {'text': 'Mexico City', 'is_correct': True},
                            {'text': 'Guadalajara', 'is_correct': False},
                            {'text': 'Monterrey', 'is_correct': False},
                            {'text': 'Puebla', 'is_correct': False},
                        ]
                    },
                    {
                        'text': 'Which is the largest country in Asia?',
                        'difficulty': 'medium',
                        'explanation': 'China is the largest country in Asia by area.',
                        'choices': [
                            {'text': 'China', 'is_correct': True},
                            {'text': 'India', 'is_correct': False},
                            {'text': 'Russia', 'is_correct': False},
                            {'text': 'Saudi Arabia', 'is_correct': False},
                        ]
                    }
                ]
            }
        ]

        try:
            with transaction.atomic():
                # Create categories and questions
                for category_data in categories_data:
                    # Create category
                    category = Category.objects.create(
                        name=category_data['name'],
                        description=category_data['description'],
                        icon=category_data['icon']
                    )
                    self.stdout.write(f'Created category: {category.name}')

                    # Create questions for this category
                    for question_data in category_data['questions']:
                        question = Question.objects.create(
                            category=category,
                            text=question_data['text'],
                            difficulty=question_data['difficulty'],
                            explanation=question_data['explanation']
                        )

                        # Create choices for this question
                        for choice_data in question_data['choices']:
                            Choice.objects.create(
                                question=question,
                                text=choice_data['text'],
                                is_correct=choice_data['is_correct']
                            )
                        self.stdout.write(f'  Created question: {question.text[:50]}...')

            self.stdout.write(self.style.SUCCESS('Successfully created categories and questions!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error creating data: {str(e)}')) 