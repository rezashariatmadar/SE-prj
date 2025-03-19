"""
Integration tests for the Quiz App.

This module contains tests that verify the end-to-end functionality
of the quiz application by simulating user interactions through the
entire quiz flow.
"""

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from quiz_app.models import Category, Question, Choice, QuizAttempt, QuizResponse


class QuizFlowTests(TestCase):
    """Integration tests for the quiz flow."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create a user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Create a category
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
                difficulty="medium",
                explanation=f"Explanation for question {i+1}"
            )
            self.questions.append(question)
            
            # Create choices for each question (one correct, three incorrect)
            correct_choice = Choice.objects.create(
                question=question,
                text="Correct Answer",
                is_correct=True
            )
            
            for j in range(3):
                Choice.objects.create(
                    question=question,
                    text=f"Incorrect Answer {j+1}",
                    is_correct=False
                )
    
    def test_anonymous_user_quiz_flow(self):
        """Test the complete quiz flow for an anonymous user."""
        # Step 1: Visit the home page
        response = self.client.get(reverse('quiz:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/index.html')
        self.assertContains(response, self.category.name)
        
        # Step 2: Start a quiz
        response = self.client.post(reverse('quiz:start'), {
            'category': self.category.id,
            'num_questions': 3
        })
        self.assertRedirects(response, reverse('quiz:question'))
        
        # A new quiz attempt should have been created
        self.assertEqual(QuizAttempt.objects.count(), 1)
        quiz_attempt = QuizAttempt.objects.first()
        self.assertIsNone(quiz_attempt.user)
        self.assertEqual(quiz_attempt.category, self.category)
        self.assertEqual(quiz_attempt.total_questions, 3)
        
        # Step 3: Answer each question
        for i in range(3):
            # Get the question page
            response = self.client.get(reverse('quiz:question'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'quiz_app/question.html')
            
            # The current question should be in the context
            question = response.context['question']
            self.assertEqual(question, self.questions[i])
            
            # Get the correct choice for this question
            correct_choice = question.choice_set.get(is_correct=True)
            
            # Submit the answer
            response = self.client.post(reverse('quiz:question'), {
                'choice': correct_choice.id
            })
            self.assertRedirects(response, reverse('quiz:question'))
        
        # Step 4: After answering all questions, should redirect to results
        response = self.client.get(reverse('quiz:question'))
        
        # Quiz attempt should be completed
        quiz_attempt.refresh_from_db()
        self.assertIsNotNone(quiz_attempt.completed_at)
        
        # Should redirect to results page
        self.assertRedirects(response, reverse('quiz:results', args=[quiz_attempt.id]))
        
        # Step 5: View the results page
        response = self.client.get(reverse('quiz:results', args=[quiz_attempt.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/results.html')
        
        # Check that the quiz attempt is in the context
        self.assertEqual(response.context['quiz_attempt'], quiz_attempt)
        
        # All answers should be correct
        self.assertEqual(quiz_attempt.score, 3)
        self.assertEqual(quiz_attempt.score_percentage(), 100.0)
    
    def test_authenticated_user_quiz_flow(self):
        """Test the complete quiz flow for an authenticated user."""
        # Log in
        self.client.login(username="testuser", password="testpassword")
        
        # Step 1: Visit the home page
        response = self.client.get(reverse('quiz:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/index.html')
        self.assertContains(response, self.category.name)
        
        # Step 2: Start a quiz
        response = self.client.post(reverse('quiz:start'), {
            'category': self.category.id,
            'num_questions': 3
        })
        self.assertRedirects(response, reverse('quiz:question'))
        
        # A new quiz attempt should have been created
        self.assertEqual(QuizAttempt.objects.count(), 1)
        quiz_attempt = QuizAttempt.objects.first()
        self.assertEqual(quiz_attempt.user, self.user)
        self.assertEqual(quiz_attempt.category, self.category)
        self.assertEqual(quiz_attempt.total_questions, 3)
        
        # Step 3: Answer each question (some correct, some incorrect)
        for i in range(3):
            # Get the question page
            response = self.client.get(reverse('quiz:question'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'quiz_app/question.html')
            
            # The current question should be in the context
            question = response.context['question']
            self.assertEqual(question, self.questions[i])
            
            # For the first two questions, select the correct answer
            # For the last question, select an incorrect answer
            if i < 2:
                choice = question.choice_set.get(is_correct=True)
            else:
                choice = question.choice_set.filter(is_correct=False).first()
            
            # Submit the answer
            response = self.client.post(reverse('quiz:question'), {
                'choice': choice.id
            })
            self.assertRedirects(response, reverse('quiz:question'))
        
        # Step 4: After answering all questions, should redirect to results
        response = self.client.get(reverse('quiz:question'))
        
        # Quiz attempt should be completed
        quiz_attempt.refresh_from_db()
        self.assertIsNotNone(quiz_attempt.completed_at)
        
        # Should redirect to results page
        self.assertRedirects(response, reverse('quiz:results', args=[quiz_attempt.id]))
        
        # Step 5: View the results page
        response = self.client.get(reverse('quiz:results', args=[quiz_attempt.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/results.html')
        
        # Check that the quiz attempt is in the context
        self.assertEqual(response.context['quiz_attempt'], quiz_attempt)
        
        # Score should be 2 out of 3
        self.assertEqual(quiz_attempt.score, 2)
        self.assertEqual(quiz_attempt.score_percentage(), 66.66666666666666)
        
        # Step 6: Visit the user stats page
        response = self.client.get(reverse('quiz:user_stats'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz_app/user_stats.html')
        
        # Check that the quiz attempt data is reflected in the stats
        self.assertEqual(response.context['total_quizzes'], 1)
        self.assertEqual(response.context['avg_score'], 66.66666666666666)
        self.assertEqual(response.context['categories_attempted'], 1)
        self.assertEqual(response.context['best_category'], self.category.name)
    
    def test_multiple_quiz_attempts(self):
        """Test multiple quiz attempts for the same user."""
        # Log in
        self.client.login(username="testuser", password="testpassword")
        
        # Complete two quizzes
        for attempt in range(2):
            # Start a quiz
            response = self.client.post(reverse('quiz:start'), {
                'category': self.category.id,
                'num_questions': 3
            })
            self.assertRedirects(response, reverse('quiz:question'))
            
            # Answer each question
            for i in range(3):
                response = self.client.get(reverse('quiz:question'))
                question = response.context['question']
                
                # Choose correct answers for all questions in the first attempt
                # and for 1 question in the second attempt
                if attempt == 0 or i == 0:
                    choice = question.choice_set.get(is_correct=True)
                else:
                    choice = question.choice_set.filter(is_correct=False).first()
                
                response = self.client.post(reverse('quiz:question'), {
                    'choice': choice.id
                })
            
            # Get the final redirect
            self.client.get(reverse('quiz:question'))
        
        # There should be 2 completed quiz attempts
        quiz_attempts = QuizAttempt.objects.filter(user=self.user)
        self.assertEqual(quiz_attempts.count(), 2)
        
        # The first attempt should have a score of 3/3
        first_attempt = quiz_attempts.order_by('started_at')[0]
        self.assertEqual(first_attempt.score, 3)
        self.assertEqual(first_attempt.score_percentage(), 100.0)
        
        # The second attempt should have a score of 1/3
        second_attempt = quiz_attempts.order_by('started_at')[1]
        self.assertEqual(second_attempt.score, 1)
        self.assertEqual(second_attempt.score_percentage(), 33.33333333333333)
        
        # Visit the user stats page
        response = self.client.get(reverse('quiz:user_stats'))
        self.assertEqual(response.status_code, 200)
        
        # Check that both quiz attempts are reflected in the stats
        self.assertEqual(response.context['total_quizzes'], 2)
        self.assertEqual(response.context['avg_score'], 66.66666666666666)  # (100 + 33.3) / 2
        self.assertEqual(response.context['categories_attempted'], 1)
        
        # Category chart and time chart should be present
        self.assertIn('category_chart', response.context)
        self.assertIn('time_chart', response.context) 