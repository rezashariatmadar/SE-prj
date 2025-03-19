"""
Tests for the Quiz application.

This module contains tests for the models, views, and forms of the quiz application.
Tests are organized into test classes for each component of the application.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from .models import Category, Question, Choice, QuizAttempt, QuizResponse


class CategoryModelTests(TestCase):
    """Tests for the Category model."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(
            name="Science",
            description="Test your science knowledge",
            icon="fa-flask"
        )
    
    def test_category_creation(self):
        """Test that a category can be created and retrieved."""
        self.assertEqual(self.category.name, "Science")
        self.assertEqual(self.category.description, "Test your science knowledge")
        self.assertEqual(self.category.icon, "fa-flask")
    
    def test_question_count_with_no_questions(self):
        """Test that question_count returns 0 when there are no questions."""
        self.assertEqual(self.category.question_count(), 0)
    
    def test_question_count_with_questions(self):
        """Test that question_count returns the correct count when there are questions."""
        # Create a question for the category
        question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            difficulty="easy"
        )
        self.assertEqual(self.category.question_count(), 1)
        
        # Add another question
        question2 = Question.objects.create(
            category=self.category,
            text="What is the chemical symbol for gold?",
            difficulty="medium"
        )
        self.assertEqual(self.category.question_count(), 2)


class QuestionModelTests(TestCase):
    """Tests for the Question model."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Science")
        self.question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            explanation="H2O is the chemical formula for water",
            difficulty="easy"
        )
        
        # Create choices for the question
        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="Water",
            is_correct=True
        )
        self.wrong_choice = Choice.objects.create(
            question=self.question,
            text="Carbon dioxide",
            is_correct=False
        )
    
    def test_question_creation(self):
        """Test that a question can be created and retrieved."""
        self.assertEqual(self.question.text, "What is H2O?")
        self.assertEqual(self.question.explanation, "H2O is the chemical formula for water")
        self.assertEqual(self.question.difficulty, "easy")
        self.assertEqual(self.question.category, self.category)
    
    def test_correct_choice(self):
        """Test that correct_choice returns the right choice."""
        self.assertEqual(self.question.correct_choice(), self.correct_choice)
    
    def test_string_representation(self):
        """Test the string representation of a question."""
        self.assertEqual(str(self.question), "What is H2O?")


class ChoiceModelTests(TestCase):
    """Tests for the Choice model."""
    
    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Science")
        self.question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            difficulty="easy"
        )
    
    def test_choice_creation(self):
        """Test that a choice can be created and retrieved."""
        choice = Choice.objects.create(
            question=self.question,
            text="Water",
            is_correct=True
        )
        self.assertEqual(choice.text, "Water")
        self.assertTrue(choice.is_correct)
        self.assertEqual(choice.question, self.question)
    
    def test_only_one_correct_choice(self):
        """Test that only one choice can be marked as correct for a question."""
        choice1 = Choice.objects.create(
            question=self.question,
            text="Water",
            is_correct=True
        )
        choice2 = Choice.objects.create(
            question=self.question,
            text="Carbon dioxide",
            is_correct=True  # This should make choice1 no longer correct
        )
        
        # Refresh choice1 from the database
        choice1.refresh_from_db()
        
        # Only choice2 should be correct now
        self.assertFalse(choice1.is_correct)
        self.assertTrue(choice2.is_correct)


class QuizAttemptModelTests(TestCase):
    """Tests for the QuizAttempt model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name="Science")
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=5
        )
        
        # Create a question and choices
        self.question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            difficulty="easy"
        )
        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="Water",
            is_correct=True
        )
        self.wrong_choice = Choice.objects.create(
            question=self.question,
            text="Carbon dioxide",
            is_correct=False
        )
    
    def test_quiz_attempt_creation(self):
        """Test that a quiz attempt can be created and retrieved."""
        self.assertEqual(self.quiz_attempt.user, self.user)
        self.assertEqual(self.quiz_attempt.category, self.category)
        self.assertEqual(self.quiz_attempt.total_questions, 5)
        self.assertEqual(self.quiz_attempt.score, 0)
        self.assertIsNone(self.quiz_attempt.completed_at)
    
    def test_is_complete(self):
        """Test is_complete method."""
        self.assertFalse(self.quiz_attempt.is_complete())
        
        # Complete the quiz
        self.quiz_attempt.completed_at = timezone.now()
        self.quiz_attempt.save()
        self.assertTrue(self.quiz_attempt.is_complete())
    
    def test_calculate_score(self):
        """Test calculate_score method."""
        # Create a correct response
        correct_response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=self.question,
            selected_choice=self.correct_choice
        )
        
        # Calculate the score
        score = self.quiz_attempt.calculate_score()
        
        # Score should be 1
        self.assertEqual(score, 1)
        self.assertEqual(self.quiz_attempt.score, 1)
    
    def test_score_percentage(self):
        """Test score_percentage method."""
        # Create a correct response
        correct_response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=self.question,
            selected_choice=self.correct_choice
        )
        
        # Calculate the score
        self.quiz_attempt.calculate_score()
        
        # Score percentage should be 20% (1 out of 5)
        self.assertEqual(self.quiz_attempt.score_percentage(), 20.0)


class QuizResponseModelTests(TestCase):
    """Tests for the QuizResponse model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.category = Category.objects.create(name="Science")
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=5
        )
        
        # Create a question and choices
        self.question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            difficulty="easy"
        )
        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="Water",
            is_correct=True
        )
        self.wrong_choice = Choice.objects.create(
            question=self.question,
            text="Carbon dioxide",
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
        self.assertEqual(response.quiz_attempt, self.quiz_attempt)
        self.assertEqual(response.question, self.question)
        self.assertEqual(response.selected_choice, self.correct_choice)
    
    def test_incorrect_response(self):
        """Test creating an incorrect response."""
        response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=self.question,
            selected_choice=self.wrong_choice
        )
        
        self.assertFalse(response.is_correct)
        self.assertEqual(response.quiz_attempt, self.quiz_attempt)
        self.assertEqual(response.question, self.question)
        self.assertEqual(response.selected_choice, self.wrong_choice)


class IndexViewTests(TestCase):
    """Tests for the IndexView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            name="Science",
            description="Test your science knowledge",
            icon="fa-flask"
        )
        
        # Create a question for the category
        self.question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            difficulty="easy"
        )
    
    def test_index_view(self):
        """Test that the index view returns a successful response."""
        response = self.client.get(reverse('quiz:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/index.html')
        self.assertContains(response, "Science")
        self.assertContains(response, "Test your science knowledge")
        
        # Context should include categories and form
        self.assertIn('categories', response.context)
        self.assertIn('form', response.context)
        self.assertEqual(list(response.context['categories']), [self.category])


class CategoryListViewTests(TestCase):
    """Tests for the CategoryListView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            name="Science",
            description="Test your science knowledge",
            icon="fa-flask"
        )
        
        # Create a question for the category
        self.question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            difficulty="easy"
        )
        
        # Create an empty category (no questions)
        self.empty_category = Category.objects.create(
            name="Empty Category",
            description="This category has no questions",
            icon="fa-question"
        )
    
    def test_category_list_view(self):
        """Test that the category list view returns a successful response."""
        response = self.client.get(reverse('quiz:categories'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/category_list.html')
        
        # Should include categories with questions but not empty ones
        self.assertContains(response, "Science")
        self.assertNotContains(response, "Empty Category")
        
        # Context should include categories
        self.assertIn('categories', response.context)
        self.assertEqual(list(response.context['categories']), [self.category])


class QuizStartViewTests(TestCase):
    """Tests for the QuizStartView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(
            name="Science",
            description="Test your science knowledge",
            icon="fa-flask"
        )
        
        # Create questions for the category
        for i in range(10):
            question = Question.objects.create(
                category=self.category,
                text=f"Question {i+1}",
                difficulty="easy"
            )
            correct_choice = Choice.objects.create(
                question=question,
                text=f"Correct answer {i+1}",
                is_correct=True
            )
            wrong_choice = Choice.objects.create(
                question=question,
                text=f"Wrong answer {i+1}",
                is_correct=False
            )
    
    def test_quiz_start_view(self):
        """Test starting a quiz."""
        response = self.client.post(
            reverse('quiz:start'),
            {
                'category': self.category.id,
                'num_questions': 5
            }
        )
        
        # Should redirect to the question view
        self.assertRedirects(response, reverse('quiz:question'))
        
        # Session should contain quiz data
        self.assertIn('quiz_questions', self.client.session)
        self.assertIn('current_question_index', self.client.session)
        self.assertIn('quiz_attempt_id', self.client.session)
        
        # Quiz attempt should be created
        quiz_attempt_id = self.client.session['quiz_attempt_id']
        quiz_attempt = QuizAttempt.objects.get(id=quiz_attempt_id)
        self.assertEqual(quiz_attempt.category, self.category)
        self.assertEqual(quiz_attempt.total_questions, 5)


class QuestionViewTests(TestCase):
    """Tests for the QuestionView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(name="Science")
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create questions and choices
        self.questions = []
        for i in range(3):
            question = Question.objects.create(
                category=self.category,
                text=f"Question {i+1}",
                difficulty="easy"
            )
            self.questions.append(question)
            
            correct_choice = Choice.objects.create(
                question=question,
                text=f"Correct answer {i+1}",
                is_correct=True
            )
            wrong_choice = Choice.objects.create(
                question=question,
                text=f"Wrong answer {i+1}",
                is_correct=False
            )
        
        # Create a quiz attempt
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
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
        """Test retrieving a question."""
        response = self.client.get(reverse('quiz:question'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/question.html')
        
        # Context should include question data
        self.assertIn('question', response.context)
        self.assertIn('choices', response.context)
        self.assertIn('question_number', response.context)
        self.assertIn('total_questions', response.context)
        self.assertIn('progress_percentage', response.context)
        
        # Question should be the first one
        self.assertEqual(response.context['question'], self.questions[0])
        self.assertEqual(response.context['question_number'], 1)
        self.assertEqual(response.context['total_questions'], 3)
    
    def test_question_view_post(self):
        """Test submitting an answer."""
        # Get the correct choice for the first question
        correct_choice = self.questions[0].correct_choice()
        
        response = self.client.post(
            reverse('quiz:question'),
            {'choice': correct_choice.id}
        )
        
        # Should redirect to the next question
        self.assertRedirects(response, reverse('quiz:question'))
        
        # Current question index should be incremented
        self.assertEqual(self.client.session['current_question_index'], 1)
        
        # A response should be recorded
        self.assertEqual(QuizResponse.objects.count(), 1)
        response_obj = QuizResponse.objects.first()
        self.assertEqual(response_obj.quiz_attempt, self.quiz_attempt)
        self.assertEqual(response_obj.question, self.questions[0])
        self.assertEqual(response_obj.selected_choice, correct_choice)
        self.assertTrue(response_obj.is_correct)
    
    def test_completing_quiz(self):
        """Test completing all questions in a quiz."""
        # Answer all questions
        for i in range(3):
            correct_choice = self.questions[i].correct_choice()
            
            # Set the current question index in the session
            session = self.client.session
            session['current_question_index'] = i
            session.save()
            
            response = self.client.post(
                reverse('quiz:question'),
                {'choice': correct_choice.id}
            )
            
            if i < 2:
                # Should redirect back to the question view
                self.assertRedirects(response, reverse('quiz:question'))
            else:
                # Last question should redirect to results
                self.assertRedirects(
                    response, 
                    reverse('quiz:results', kwargs={'quiz_id': self.quiz_attempt.id})
                )
        
        # Quiz should be marked as complete
        self.quiz_attempt.refresh_from_db()
        self.assertTrue(self.quiz_attempt.is_complete())
        self.assertEqual(self.quiz_attempt.score, 3)  # All answers were correct
        
        # Session should be cleared
        self.assertNotIn('quiz_questions', self.client.session)
        self.assertNotIn('current_question_index', self.client.session)
        self.assertNotIn('quiz_attempt_id', self.client.session)


class ResultsViewTests(TestCase):
    """Tests for the ResultsView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(name="Science")
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Create a question and choices
        self.question = Question.objects.create(
            category=self.category,
            text="What is H2O?",
            difficulty="easy"
        )
        self.correct_choice = Choice.objects.create(
            question=self.question,
            text="Water",
            is_correct=True
        )
        self.wrong_choice = Choice.objects.create(
            question=self.question,
            text="Carbon dioxide",
            is_correct=False
        )
        
        # Create a completed quiz attempt
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=1,
            score=1,
            completed_at=timezone.now()
        )
        
        # Create a response
        self.response = QuizResponse.objects.create(
            quiz_attempt=self.quiz_attempt,
            question=self.question,
            selected_choice=self.correct_choice
        )
    
    def test_results_view(self):
        """Test viewing quiz results."""
        response = self.client.get(
            reverse('quiz:results', kwargs={'quiz_id': self.quiz_attempt.id})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/results.html')
        
        # Context should include quiz attempt and responses
        self.assertIn('quiz_attempt', response.context)
        self.assertEqual(response.context['quiz_attempt'], self.quiz_attempt)
        
        # Results page should show score
        self.assertContains(response, "score")
        
        # Results page should include visualizations
        if self.response.is_correct:  # Only if response exists and is correct
            self.assertIn('performance_chart', response.context)


class UserStatsViewTests(TestCase):
    """Tests for the UserStatsView."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        self.category = Category.objects.create(name="Science")
        
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        
        # Log in the user
        self.client.login(username='testuser', password='testpassword')
        
        # Create a completed quiz attempt
        self.quiz_attempt = QuizAttempt.objects.create(
            user=self.user,
            category=self.category,
            total_questions=5,
            score=4,
            completed_at=timezone.now()
        )
    
    def test_user_stats_view_authenticated(self):
        """Test that authenticated users can view their stats."""
        response = self.client.get(reverse('quiz:user_stats'))
        
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/user_stats.html')
        
        # Context should include user stats
        self.assertIn('total_quizzes', response.context)
        self.assertEqual(response.context['total_quizzes'], 1)
        
        # Stats page should show user's stats
        self.assertContains(response, "Quizzes Completed")
        self.assertContains(response, "Average Score")
    
    def test_user_stats_view_unauthenticated(self):
        """Test that unauthenticated users are redirected to login."""
        # Log out the user
        self.client.logout()
        
        response = self.client.get(reverse('quiz:user_stats'))
        
        # Should redirect to login page
        login_url = reverse('login')
        self.assertRedirects(
            response, 
            f'{login_url}?next={reverse("quiz:user_stats")}'
        ) 