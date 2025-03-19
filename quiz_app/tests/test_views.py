"""
Tests for Quiz App views.

This module contains tests for the views used in the quiz application:
- IndexView
- CategoryListView
- QuizStartView
- QuestionView
- ResultsView
- UserStatsView
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
import json

from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse


class IndexViewTests(TestCase):
    """Tests for the IndexView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.url = reverse('quiz:index')
        
        # Create a category with questions
        self.category = Category.objects.create(
            name="Test Category",
            description="This is a test category",
            icon="fa-test"
        )
        
        self.question = Question.objects.create(
            category=self.category,
            text="Test Question",
            difficulty="medium"
        )
    
    def test_index_view_with_no_categories(self):
        """Test the index view when there are no categories with questions."""
        # Delete the question so that the category has no questions
        self.question.delete()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/index.html')
        self.assertQuerysetEqual(response.context['categories'], [])
    
    def test_index_view_with_categories(self):
        """Test the index view when there are categories with questions."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/index.html')
        self.assertQuerysetEqual(response.context['categories'], [self.category])
        self.assertContains(response, self.category.name)


class CategoryListViewTests(TestCase):
    """Tests for the CategoryListView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.url = reverse('quiz:categories')
        
        # Create a category with questions
        self.category = Category.objects.create(
            name="Test Category",
            description="This is a test category",
            icon="fa-test"
        )
        
        self.question = Question.objects.create(
            category=self.category,
            text="Test Question",
            difficulty="medium"
        )
    
    def test_category_list_view(self):
        """Test the category list view."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/category_list.html')
        self.assertQuerysetEqual(response.context['categories'], [self.category])
        self.assertContains(response, self.category.name)
    
    def test_category_list_view_with_no_questions(self):
        """Test the category list view when a category has no questions."""
        # Delete the question so that the category has no questions
        self.question.delete()
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/category_list.html')
        self.assertQuerysetEqual(response.context['categories'], [])


class QuizStartViewTests(TestCase):
    """Tests for the QuizStartView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.url = reverse('quiz:start')
        
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Create a category with questions
        self.category = Category.objects.create(
            name="Test Category",
            description="This is a test category",
            icon="fa-test"
        )
        
        # Create multiple questions
        for i in range(5):
            question = Question.objects.create(
                category=self.category,
                text=f"Test Question {i+1}",
                difficulty="medium"
            )
            
            # Create choices for each question
            Choice.objects.create(
                question=question,
                text="Correct Answer",
                is_correct=True
            )
            
            Choice.objects.create(
                question=question,
                text="Incorrect Answer",
                is_correct=False
            )
    
    def test_quiz_start_view_authenticated(self):
        """Test starting a quiz as an authenticated user."""
        self.client.login(username="testuser", password="testpassword")
        
        response = self.client.post(self.url, {
            'category': self.category.id,
            'num_questions': 3
        })
        
        # Should redirect to the question page
        self.assertRedirects(response, reverse('quiz:question'))
        
        # A quiz attempt should have been created
        self.assertEqual(QuizAttempt.objects.count(), 1)
        quiz_attempt = QuizAttempt.objects.first()
        self.assertEqual(quiz_attempt.user, self.user)
        self.assertEqual(quiz_attempt.category, self.category)
        self.assertEqual(quiz_attempt.total_questions, 3)
        
        # Session should have quiz data
        session = self.client.session
        self.assertIn('quiz_questions', session)
        self.assertEqual(len(session['quiz_questions']), 3)
        self.assertEqual(session['current_question_index'], 0)
        self.assertEqual(session['quiz_attempt_id'], quiz_attempt.id)
    
    def test_quiz_start_view_anonymous(self):
        """Test starting a quiz as an anonymous user."""
        response = self.client.post(self.url, {
            'category': self.category.id,
            'num_questions': 3
        })
        
        # Should redirect to the question page
        self.assertRedirects(response, reverse('quiz:question'))
        
        # A quiz attempt should have been created
        self.assertEqual(QuizAttempt.objects.count(), 1)
        quiz_attempt = QuizAttempt.objects.first()
        self.assertIsNone(quiz_attempt.user)
        self.assertEqual(quiz_attempt.category, self.category)
        self.assertEqual(quiz_attempt.total_questions, 3)
        
        # Session should have quiz data
        session = self.client.session
        self.assertIn('quiz_questions', session)
        self.assertEqual(len(session['quiz_questions']), 3)
        self.assertEqual(session['current_question_index'], 0)
        self.assertEqual(session['quiz_attempt_id'], quiz_attempt.id)
    
    def test_quiz_start_view_invalid_form(self):
        """Test starting a quiz with an invalid form."""
        response = self.client.post(self.url, {
            'category': 999,  # Invalid category ID
            'num_questions': 3
        })
        
        # Should redirect to the index page
        self.assertRedirects(response, reverse('quiz:index'))
        
        # No quiz attempt should have been created
        self.assertEqual(QuizAttempt.objects.count(), 0)


class QuestionViewTests(TestCase):
    """Tests for the QuestionView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.url = reverse('quiz:question')
        
        # Create a category with questions
        self.category = Category.objects.create(
            name="Test Category",
            description="This is a test category",
            icon="fa-test"
        )
        
        # Create questions and choices
        self.questions = []
        for i in range(3):
            question = Question.objects.create(
                category=self.category,
                text=f"Test Question {i+1}",
                difficulty="medium"
            )
            self.questions.append(question)
            
            # Create choices for each question
            Choice.objects.create(
                question=question,
                text="Correct Answer",
                is_correct=True
            )
            
            Choice.objects.create(
                question=question,
                text="Incorrect Answer",
                is_correct=False
            )
        
        # Create a quiz attempt
        self.quiz_attempt = QuizAttempt.objects.create(
            user=None,
            category=self.category,
            total_questions=3
        )
        
        # Set up the session
        session = self.client.session
        session['quiz_questions'] = [q.id for q in self.questions]
        session['current_question_index'] = 0
        session['quiz_attempt_id'] = self.quiz_attempt.id
        session.save()
    
    def test_question_view_get(self):
        """Test viewing a question."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/question.html')
        
        # Check context
        self.assertEqual(response.context['quiz_attempt'], self.quiz_attempt)
        self.assertEqual(response.context['question'], self.questions[0])
        self.assertEqual(response.context['question_number'], 1)
        self.assertEqual(response.context['total_questions'], 3)
        self.assertEqual(response.context['progress_percentage'], 0)
    
    def test_question_view_post(self):
        """Test answering a question."""
        # Get the current question and its correct choice
        question = self.questions[0]
        correct_choice = question.choice_set.get(is_correct=True)
        
        response = self.client.post(self.url, {
            'choice': correct_choice.id
        })
        
        # Should redirect back to the question page
        self.assertRedirects(response, self.url)
        
        # A response should have been created
        self.assertEqual(QuizResponse.objects.count(), 1)
        quiz_response = QuizResponse.objects.first()
        self.assertEqual(quiz_response.quiz_attempt, self.quiz_attempt)
        self.assertEqual(quiz_response.question, question)
        self.assertEqual(quiz_response.selected_choice, correct_choice)
        self.assertTrue(quiz_response.is_correct)
        
        # The current question index should have been incremented
        session = self.client.session
        self.assertEqual(session['current_question_index'], 1)
    
    def test_question_view_last_question(self):
        """Test answering the last question."""
        # Set the current question index to the last question
        session = self.client.session
        session['current_question_index'] = 2
        session.save()
        
        # Get the current question and its correct choice
        question = self.questions[2]
        correct_choice = question.choice_set.get(is_correct=True)
        
        response = self.client.post(self.url, {
            'choice': correct_choice.id
        })
        
        # Should redirect to the results page
        self.assertRedirects(response, self.url)
        
        # Get the response again to check the redirect to results
        response = self.client.get(self.url)
        
        # Quiz attempt should be completed and redirected to results
        self.quiz_attempt.refresh_from_db()
        self.assertIsNotNone(self.quiz_attempt.completed_at)
        self.assertRedirects(response, reverse('quiz:results', args=[self.quiz_attempt.id]))
        
        # Session variables should be cleared
        session = self.client.session
        self.assertNotIn('quiz_questions', session)
        self.assertNotIn('current_question_index', session)
        self.assertNotIn('quiz_attempt_id', session)
    
    def test_question_view_no_active_quiz(self):
        """Test viewing a question with no active quiz."""
        # Clear the session
        session = self.client.session
        for key in ['quiz_questions', 'current_question_index', 'quiz_attempt_id']:
            if key in session:
                del session[key]
        session.save()
        
        response = self.client.get(self.url)
        
        # Should redirect to the index page
        self.assertRedirects(response, reverse('quiz:index'))


class ResultsViewTests(TestCase):
    """Tests for the ResultsView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Create a category with questions
        self.category = Category.objects.create(
            name="Test Category",
            description="This is a test category",
            icon="fa-test"
        )
        
        # Create a quiz attempt
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=3,
            score=2,
            completed_at=timezone.now()
        )
        
        # Create questions and responses
        for i in range(3):
            question = Question.objects.create(
                category=self.category,
                text=f"Test Question {i+1}",
                difficulty="medium"
            )
            
            # Create choices for each question
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
            
            # Create a response for each question
            QuizResponse.objects.create(
                quiz_attempt=self.quiz_attempt,
                question=question,
                selected_choice=correct_choice if i < 2 else incorrect_choice
            )
        
        self.url = reverse('quiz:results', args=[self.quiz_attempt.id])
    
    def test_results_view(self):
        """Test viewing quiz results."""
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/results.html')
        
        # Check context
        self.assertEqual(response.context['quiz_attempt'], self.quiz_attempt)
        self.assertIn('responses', response.context)
        self.assertEqual(len(response.context['responses']), 3)
        
        # Check that the performance chart is in the context
        self.assertIn('performance_chart', response.context)


class UserStatsViewTests(TestCase):
    """Tests for the UserStatsView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.url = reverse('quiz:user_stats')
        
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Create categories
        self.category1 = Category.objects.create(name="Category 1")
        self.category2 = Category.objects.create(name="Category 2")
        
        # Create quiz attempts
        self.quiz_attempt1 = QuizAttempt.objects.create(
            user=self.user,
            category=self.category1,
            total_questions=5,
            score=4,
            completed_at=timezone.now()
        )
        
        self.quiz_attempt2 = QuizAttempt.objects.create(
            user=self.user,
            category=self.category2,
            total_questions=5,
            score=3,
            completed_at=timezone.now()
        )
    
    def test_user_stats_view_authenticated(self):
        """Test viewing user stats as an authenticated user."""
        self.client.login(username="testuser", password="testpassword")
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/user_stats.html')
        
        # Check context
        self.assertEqual(response.context['total_quizzes'], 2)
        self.assertEqual(response.context['avg_score'], 70.0)  # (80 + 60) / 2
        self.assertEqual(response.context['categories_attempted'], 2)
        self.assertEqual(response.context['best_category'], "Category 1")
        
        # Check that the charts are in the context
        self.assertIn('time_chart', response.context)
        self.assertIn('category_chart', response.context)
    
    def test_user_stats_view_unauthenticated(self):
        """Test viewing user stats as an unauthenticated user."""
        response = self.client.get(self.url)
        
        # Should redirect to the login page
        login_url = reverse('login')
        self.assertRedirects(response, f'{login_url}?next={self.url}') 