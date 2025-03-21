"""
Tests for the forms in the Quiz application.
"""

from django.test import TestCase
from django.contrib.auth.models import User

from quiz_app.models import Category
from quiz_app.forms import QuizSelectionForm, UserRegistrationForm


class FormTests(TestCase):
    """Tests for the forms of the Quiz application."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test category
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description',
            icon='fa-test'
        )
        
        # Create test questions
        for i in range(5):
            question = self.category.question_set.create(
                text=f'Test Question {i}',
                difficulty='medium',
                explanation=f'Test Explanation {i}'
            )
            
            # Create choices for each question
            question.choice_set.create(
                text=f'Correct Choice {i}',
                is_correct=True
            )
            
            for j in range(3):
                question.choice_set.create(
                    text=f'Incorrect Choice {i}-{j}',
                    is_correct=False
                )
    
    def test_quiz_selection_form_valid(self):
        """Test that a valid QuizSelectionForm is valid."""
        form = QuizSelectionForm(data={
            'category': self.category.id,
            'num_questions': 5
        })
        self.assertTrue(form.is_valid())
        
    def test_quiz_selection_form_invalid_category(self):
        """Test that a QuizSelectionForm with an invalid category is invalid."""
        form = QuizSelectionForm(data={
            'category': 999,  # Non-existent category
            'num_questions': 5
        })
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        
    def test_quiz_selection_form_invalid_num_questions(self):
        """Test that a QuizSelectionForm with an invalid number of questions is invalid."""
        # Too few questions
        form = QuizSelectionForm(data={
            'category': self.category.id,
            'num_questions': 3
        })
        self.assertFalse(form.is_valid())
        self.assertIn('num_questions', form.errors)
        
        # Too many questions
        form = QuizSelectionForm(data={
            'category': self.category.id,
            'num_questions': 25
        })
        self.assertFalse(form.is_valid())
        self.assertIn('num_questions', form.errors)
        
    def test_user_registration_form_valid(self):
        """Test that a valid UserRegistrationForm is valid."""
        form = UserRegistrationForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        })
        self.assertTrue(form.is_valid())
        
    def test_user_registration_form_passwords_dont_match(self):
        """Test that a UserRegistrationForm with non-matching passwords is invalid."""
        form = UserRegistrationForm(data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'DifferentPassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
        
    def test_user_registration_form_username_taken(self):
        """Test that a UserRegistrationForm with a taken username is invalid."""
        # Create a user with the username 'existinguser'
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='TestPassword123'
        )
        
        # Try to create another user with the same username
        form = UserRegistrationForm(data={
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password1': 'TestPassword123',
            'password2': 'TestPassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors) 