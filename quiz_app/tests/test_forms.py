"""
Tests for Quiz App forms.

This module contains tests for the forms used in the quiz application:
- QuizSelectionForm
"""

from django.test import TestCase
from quiz_app.forms import QuizSelectionForm
from quiz_app.models import Category, Question


class QuizSelectionFormTests(TestCase):
    """Tests for the QuizSelectionForm."""
    
    def setUp(self):
        """Set up test data."""
        # Create a category with questions
        self.category = Category.objects.create(
            name="Test Category",
            description="This is a test category",
            icon="fa-test"
        )
        
        # Create 20 questions to allow testing the full range
        for i in range(20):
            Question.objects.create(
                category=self.category,
                text=f"Test Question {i+1}",
                difficulty="medium"
            )
    
    def test_quiz_selection_form_valid_data(self):
        """Test the form with valid data across the allowed range (5-20 questions)."""
        # Test minimum number of questions (5)
        form_data = {
            'category': self.category.id,
            'num_questions': 5
        }
        form = QuizSelectionForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors for 5 questions: {form.errors}")
        
        # Test middle range (10 questions)
        form_data['num_questions'] = 10
        form = QuizSelectionForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors for 10 questions: {form.errors}")
        
        # Test maximum number of questions (20)
        form_data['num_questions'] = 20
        form = QuizSelectionForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors for 20 questions: {form.errors}")
    
    def test_quiz_selection_form_blank_data(self):
        """Test the form with blank data."""
        form = QuizSelectionForm(data={})
        
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
        self.assertIn('num_questions', form.errors)
    
    def test_quiz_selection_form_invalid_category(self):
        """Test the form with an invalid category."""
        form_data = {
            'category': 999,  # Invalid category ID
            'num_questions': 10
        }
        form = QuizSelectionForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('category', form.errors)
    
    def test_quiz_selection_form_invalid_num_questions(self):
        """Test the form with an invalid number of questions."""
        # Test with too few questions (below minimum)
        form_data = {
            'category': self.category.id,
            'num_questions': 4
        }
        form = QuizSelectionForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('num_questions', form.errors)
        
        # Test with too many questions (above maximum)
        form_data['num_questions'] = 21
        form = QuizSelectionForm(data=form_data)
        
        self.assertFalse(form.is_valid())
        self.assertIn('num_questions', form.errors)
    
    def test_quiz_selection_form_choices(self):
        """Test that the form only includes categories with questions."""
        # Create a category with no questions
        empty_category = Category.objects.create(
            name="Empty Category",
            description="This category has no questions",
            icon="fa-empty"
        )
        
        form = QuizSelectionForm()
        
        # Check that the form only includes categories with questions
        category_choices = [choice[0] for choice in form.fields['category'].choices if choice[0] != '']
        
        self.assertIn(self.category.id, category_choices)
        self.assertNotIn(empty_category.id, category_choices) 