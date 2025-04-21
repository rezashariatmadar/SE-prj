"""
Tests for the quiz timer functionality.
"""

from datetime import timedelta
from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse

class QuizTimerTests(TestCase):
    """Test cases for the quiz timer feature."""
    
    def setUp(self):
        """Set up test data."""
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        
        # Create a test category
        self.category = Category.objects.create(
            name='Test Category',
            description='A category for testing'
        )
        
        # Create test questions
        self.questions = []
        for i in range(5):
            question = Question.objects.create(
                category=self.category,
                text=f'Test Question {i+1}',
                difficulty='medium'
            )
            self.questions.append(question)
            
            # Create choices for each question
            for j in range(4):
                Choice.objects.create(
                    question=question,
                    text=f'Choice {j+1}',
                    is_correct=(j == 0)  # First choice is correct
                )
        
        # Set up a client
        self.client = Client()
    
    def test_quiz_with_time_limit(self):
        """Test that a quiz can be created with a time limit."""
        self.client.login(username='testuser', password='testpassword123')
        
        # Start a quiz with a time limit
        response = self.client.post(reverse('quiz:start'), {
            'category': self.category.id,
            'num_questions': 5,
            'time_limit': 60
        })
        
        # Check that the quiz was created
        self.assertEqual(QuizAttempt.objects.count(), 1)
        
        # Get the quiz attempt
        quiz_attempt = QuizAttempt.objects.first()
        
        # Check that the time limit was set
        self.assertEqual(quiz_attempt.time_limit, 60)
    
    def test_time_remaining_calculation(self):
        """Test the time_remaining method of the QuizAttempt model."""
        # Create a quiz attempt with a time limit
        quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=5,
            time_limit=60
        )
        
        # Test that time remaining is correct for a new attempt
        self.assertLessEqual(quiz_attempt.time_remaining(), 60)
        self.assertGreater(quiz_attempt.time_remaining(), 50)  # Allow for some time to pass
        
        # Test that time remaining is 0 for a completed attempt
        quiz_attempt.completed_at = timezone.now()
        quiz_attempt.save()
        self.assertEqual(quiz_attempt.time_remaining(), 0)
        
        # Test that time remaining is 0 for an attempt with no time limit
        quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=5,
            time_limit=0
        )
        self.assertEqual(quiz_attempt.time_remaining(), 0)
    
    def test_time_limit_expiry(self):
        """Test that a quiz is automatically completed when the time limit expires."""
        self.client.login(username='testuser', password='testpassword123')
        
        # Start a quiz with a time limit
        response = self.client.post(reverse('quiz:start'), {
            'category': self.category.id,
            'num_questions': 5,
            'time_limit': 60
        })
        
        # Get the quiz attempt
        quiz_attempt = QuizAttempt.objects.first()
        
        # Manually set the started_at time to be in the past (so the time limit has expired)
        quiz_attempt.started_at = timezone.now() - timedelta(minutes=2)
        quiz_attempt.save()
        
        # Try to access the next question
        response = self.client.get(reverse('quiz:question'))
        
        # Check that we are redirected to the results page
        self.assertRedirects(response, reverse('quiz:results', kwargs={'quiz_id': quiz_attempt.id}))
        
        # Check that the quiz attempt is now completed
        quiz_attempt.refresh_from_db()
        self.assertIsNotNone(quiz_attempt.completed_at)
    
    def test_timer_display_in_template(self):
        """Test that the timer is displayed in the template when a time limit is set."""
        self.client.login(username='testuser', password='testpassword123')
        
        # Start a quiz with a time limit
        response = self.client.post(reverse('quiz:start'), {
            'category': self.category.id,
            'num_questions': 5,
            'time_limit': 60
        })
        
        # Get the first question
        response = self.client.get(reverse('quiz:question'))
        
        # Check that the timer is displayed
        self.assertContains(response, 'Time Remaining:')
        self.assertContains(response, 'id="timer"')
        
        # Start a quiz without a time limit
        response = self.client.post(reverse('quiz:start'), {
            'category': self.category.id,
            'num_questions': 5,
            'time_limit': 0
        })
        
        # Get the first question
        response = self.client.get(reverse('quiz:question'))
        
        # Check that the timer is not displayed
        self.assertNotContains(response, 'Time Remaining:')
        self.assertNotContains(response, 'id="timer"') 