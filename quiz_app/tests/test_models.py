"""
Tests for Quiz App models.

This module contains tests for the models used in the quiz application:
- Category
- Question
- Choice
- QuizAttempt
- QuizResponse
"""

from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse


class CategoryModelTests(TestCase):
    """Tests for the Category model."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Test Category",
            description="This is a test category",
            icon="fa-test"
        )
    
    def test_category_creation(self):
        """Test that a category can be created."""
        self.assertEqual(self.category.name, "Test Category")
        self.assertEqual(self.category.description, "This is a test category")
        self.assertEqual(self.category.icon, "fa-test")
    
    def test_category_str(self):
        """Test the string representation of a category."""
        self.assertEqual(str(self.category), "Test Category")
    
    def test_question_count(self):
        """Test the question_count method."""
        # Initially, there should be no questions
        self.assertEqual(self.category.question_count(), 0)
        
        # Add a question
        Question.objects.create(
            category=self.category,
            text="Test Question",
            difficulty="medium"
        )
        
        # Now there should be one question
        self.assertEqual(self.category.question_count(), 1)


class QuestionModelTests(TestCase):
    """Tests for the Question model."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Test Category")
        self.question = Question.objects.create(
            category=self.category,
            text="What is the answer to this question?",
            explanation="This is the explanation",
            difficulty="medium"
        )
        
        # Create choices for the question
        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="Correct Answer",
            is_correct=True
        )
        
        self.incorrect_choice = Choice.objects.create(
            question=self.question,
            text="Incorrect Answer",
            is_correct=False
        )
    
    def test_question_creation(self):
        """Test that a question can be created."""
        self.assertEqual(self.question.text, "What is the answer to this question?")
        self.assertEqual(self.question.explanation, "This is the explanation")
        self.assertEqual(self.question.difficulty, "medium")
        self.assertEqual(self.question.category, self.category)
    
    def test_question_str(self):
        """Test the string representation of a question."""
        self.assertEqual(str(self.question), "What is the answer to this question?")
    
    def test_correct_choice(self):
        """Test the correct_choice method."""
        self.assertEqual(self.question.correct_choice(), self.correct_choice)


class ChoiceModelTests(TestCase):
    """Tests for the Choice model."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Test Category")
        self.question = Question.objects.create(
            category=self.category,
            text="Test Question",
            difficulty="medium"
        )
        
        self.choice = Choice.objects.create(
            question=self.question,
            text="Test Choice",
            is_correct=True
        )
    
    def test_choice_creation(self):
        """Test that a choice can be created."""
        self.assertEqual(self.choice.text, "Test Choice")
        self.assertTrue(self.choice.is_correct)
        self.assertEqual(self.choice.question, self.question)
    
    def test_choice_str(self):
        """Test the string representation of a choice."""
        self.assertEqual(str(self.choice), "Test Choice")
    
    def test_unique_correct_choice(self):
        """Test that only one choice per question can be marked as correct."""
        # Create a second choice marked as correct
        new_choice = Choice.objects.create(
            question=self.question,
            text="Another Choice",
            is_correct=True
        )
        
        # The first choice should no longer be marked as correct
        self.choice.refresh_from_db()
        self.assertFalse(self.choice.is_correct)
        self.assertTrue(new_choice.is_correct)


class QuizAttemptModelTests(TestCase):
    """Tests for the QuizAttempt model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        self.category = Category.objects.create(name="Test Category")
        
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=5
        )
    
    def test_quiz_attempt_creation(self):
        """Test that a quiz attempt can be created."""
        self.assertEqual(self.quiz_attempt.user, self.user)
        self.assertEqual(self.quiz_attempt.category, self.category)
        self.assertEqual(self.quiz_attempt.total_questions, 5)
        self.assertEqual(self.quiz_attempt.score, 0)
        self.assertIsNotNone(self.quiz_attempt.started_at)
        self.assertIsNone(self.quiz_attempt.completed_at)
    
    def test_is_complete(self):
        """Test the is_complete method."""
        # Initially, the quiz should not be complete
        self.assertFalse(self.quiz_attempt.is_complete())
        
        # Complete the quiz
        self.quiz_attempt.completed_at = timezone.now()
        self.quiz_attempt.save()
        
        # Now it should be complete
        self.assertTrue(self.quiz_attempt.is_complete())
    
    def test_calculate_score(self):
        """Test the calculate_score method."""
        # Create a question and choices
        question = Question.objects.create(
            category=self.category,
            text="Test Question",
            difficulty="medium"
        )
        
        correct_choice = Choice.objects.create(
            question=question,
            text="Correct Answer",
            is_correct=True
        )
        
        incorrect_choice = Choice.objects.create(
            question=question,
            text="Incorrect Answer",
            is_correct=False
        )
        
        # Add responses to the quiz attempt
        correct_response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=question,
            selected_choice=correct_choice
        )
        
        # Calculate the score
        score = self.quiz_attempt.calculate_score()
        
        # There should be 1 correct answer
        self.assertEqual(score, 1)
        self.assertEqual(self.quiz_attempt.score, 1)
    
    def test_score_percentage(self):
        """Test the score_percentage method."""
        # Set the score
        self.quiz_attempt.score = 4
        self.quiz_attempt.total_questions = 5
        self.quiz_attempt.save()
        
        # Test the percentage
        self.assertEqual(self.quiz_attempt.score_percentage(), 80.0)
        
        # Test with zero questions
        self.quiz_attempt.total_questions = 0
        self.quiz_attempt.save()
        self.assertEqual(self.quiz_attempt.score_percentage(), 0)


class QuizResponseModelTests(TestCase):
    """Tests for the QuizResponse model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        self.category = Category.objects.create(name="Test Category")
        
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=1
        )
        
        self.question = Question.objects.create(
            category=self.category,
            text="Test Question",
            difficulty="medium"
        )
        
        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="Correct Answer",
            is_correct=True
        )
        
        self.incorrect_choice = Choice.objects.create(
            question=self.question,
            text="Incorrect Answer",
            is_correct=False
        )
    
    def test_correct_response(self):
        """Test creating a correct response."""
        response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=self.question,
            selected_choice=self.correct_choice
        )
        
        self.assertTrue(response.is_correct)
    
    def test_incorrect_response(self):
        """Test creating an incorrect response."""
        response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=self.question,
            selected_choice=self.incorrect_choice
        )
        
        self.assertFalse(response.is_correct)
    
    def test_response_str(self):
        """Test the string representation of a response."""
        response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=self.question,
            selected_choice=self.correct_choice
        )
        
        expected_str = f"Response to {self.question} in {self.quiz_attempt}"
        self.assertEqual(str(response), expected_str) 