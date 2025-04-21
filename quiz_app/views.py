"""
Views for the Quiz application.

This module defines the view functions and classes that handle HTTP requests
and return appropriate responses for the quiz application.
"""

import random
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView, UpdateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Count, Avg, Max, Min
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from django.contrib import messages

from .models import Category, Question, Choice, QuizAttempt, QuizResponse, UserProfile
from .forms import QuizSelectionForm, UserRegistrationForm


class IndexView(TemplateView):
    """
    View for the home page of the quiz application.
    
    Displays a welcome message and available quiz categories.
    """
    template_name = 'quiz_app/index.html'
    
    def get_context_data(self, **kwargs):
        """Add categories to the context."""
        context = super().get_context_data(**kwargs)
        # Get all categories with their question counts
        categories = Category.objects.annotate(
            num_questions=Count('question')
        ).filter(num_questions__gt=0)
        
        context.update({
            'categories': categories,
            'form': QuizSelectionForm(),
        })
        return context


class CategoryListView(ListView):
    """
    View to display all available quiz categories.
    """
    model = Category
    template_name = 'quiz_app/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        """Return only categories that have questions."""
        return Category.objects.annotate(
            num_questions=Count('question')
        ).filter(num_questions__gt=0)


class QuizStartView(View):
    """
    View to handle the start of a new quiz.
    
    Creates a new QuizAttempt and redirects to the first question.
    """
    def post(self, request):
        """Handle POST request with category selection."""
        form = QuizSelectionForm(request.POST)
        if form.is_valid():
            category = form.cleaned_data['category']
            num_questions = form.cleaned_data['num_questions']
            time_limit = form.cleaned_data['time_limit']
            
            # Create a new quiz attempt
            quiz_attempt = QuizAttempt(
                user=request.user if request.user.is_authenticated else None,
                category=category,
                total_questions=num_questions,
                time_limit=time_limit
            )
            quiz_attempt.save()
            
            # Select random questions from the category
            questions = list(Question.objects.filter(category=category))
            if len(questions) > num_questions:
                questions = random.sample(questions, num_questions)
            
            # Store the question IDs in the session
            request.session['quiz_questions'] = [q.id for q in questions]
            request.session['current_question_index'] = 0
            request.session['quiz_attempt_id'] = quiz_attempt.id
            
            # Redirect to the first question
            return redirect('quiz:question')
        else:
            # If form is invalid, add error messages and render index page with the form errors
            categories = Category.objects.annotate(
                num_questions=Count('question')
            ).filter(num_questions__gt=0)
            
            return render(request, 'quiz_app/index.html', {
                'form': form, 
                'categories': categories,
                'form_errors': True
            })


class QuestionView(View):
    """
    View to display a quiz question and process the answer.
    """
    template_name = 'quiz_app/question.html'
    
    def get(self, request):
        """Handle GET request to display a question."""
        # Check if there's an active quiz
        if 'quiz_questions' not in request.session:
            return redirect('quiz:index')
        
        # Get the current question index and quiz attempt
        current_index = request.session.get('current_question_index', 0)
        quiz_attempt_id = request.session.get('quiz_attempt_id')
        quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id)
        
        # Check if time limit has expired
        time_remaining = quiz_attempt.time_remaining()
        if quiz_attempt.time_limit > 0 and time_remaining <= 0 and not quiz_attempt.is_complete():
            # Time's up - complete the quiz
            quiz_attempt.completed_at = timezone.now()
            quiz_attempt.calculate_score()
            quiz_attempt.save()
            
            # Clear session data
            for key in ['quiz_questions', 'current_question_index', 'quiz_attempt_id']:
                if key in request.session:
                    del request.session[key]
            
            # Add a message
            messages.warning(request, "Time's up! Your quiz has been submitted.")
            return redirect('quiz:results', quiz_id=quiz_attempt.id)
        
        # Check if we've reached the end of the quiz
        question_ids = request.session.get('quiz_questions', [])
        if current_index >= len(question_ids):
            # Complete the quiz and redirect to results
            quiz_attempt.completed_at = timezone.now()
            quiz_attempt.calculate_score()
            quiz_attempt.save()
            
            # Clear session data
            for key in ['quiz_questions', 'current_question_index', 'quiz_attempt_id']:
                if key in request.session:
                    del request.session[key]
            
            return redirect('quiz:results', quiz_id=quiz_attempt.id)
        
        # Get the current question
        question_id = question_ids[current_index]
        question = get_object_or_404(Question, id=question_id)
        choices = question.choice_set.all()
        
        # Prepare context for the template
        context = {
            'quiz_attempt': quiz_attempt,
            'question': question,
            'choices': choices,
            'question_number': current_index + 1,
            'total_questions': len(question_ids),
            'progress_percentage': ((current_index) / len(question_ids)) * 100,
            'time_limit': quiz_attempt.time_limit,
            'time_remaining': time_remaining,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        """Handle POST request with answer submission."""
        # Check if there's an active quiz
        if 'quiz_questions' not in request.session:
            return redirect('quiz:index')
        
        # Get the current question index and quiz attempt
        current_index = request.session.get('current_question_index', 0)
        quiz_attempt_id = request.session.get('quiz_attempt_id')
        quiz_attempt = get_object_or_404(QuizAttempt, id=quiz_attempt_id)
        
        # Get the current question
        question_ids = request.session.get('quiz_questions', [])
        question_id = question_ids[current_index]
        question = get_object_or_404(Question, id=question_id)
        
        # Process the submitted answer
        choice_id = request.POST.get('choice')
        if choice_id:
            choice = get_object_or_404(Choice, id=choice_id)
            
            # Record the response
            response = QuizResponse(
                quiz_attempt=quiz_attempt,
                question=question,
                selected_choice=choice,
            )
            response.save()
            
            # Move to the next question
            request.session['current_question_index'] = current_index + 1
        
        return redirect('quiz:question')


class ResultsView(DetailView):
    """
    View to display the results of a completed quiz.
    """
    model = QuizAttempt
    template_name = 'quiz_app/results.html'
    context_object_name = 'quiz_attempt'
    pk_url_kwarg = 'quiz_id'
    
    def get_context_data(self, **kwargs):
        """Add extra context data including visualizations."""
        context = super().get_context_data(**kwargs)
        quiz_attempt = self.object
        
        # Get all responses for this attempt
        responses = QuizResponse.objects.filter(quiz_attempt=quiz_attempt)
        
        # Create a DataFrame for analysis
        if responses.exists():
            data = {
                'question': [r.question.text for r in responses],
                'is_correct': [r.is_correct for r in responses],
                'difficulty': [r.question.difficulty for r in responses]
            }
            df = pd.DataFrame(data)
            
            # Generate performance by difficulty chart
            difficulty_performance = df.groupby('difficulty')['is_correct'].mean() * 100
            
            # Create a bar chart
            plt.figure(figsize=(8, 4))
            sns.barplot(x=difficulty_performance.index, y=difficulty_performance.values)
            plt.title('Performance by Question Difficulty')
            plt.xlabel('Difficulty Level')
            plt.ylabel('Correct Answers (%)')
            plt.ylim(0, 100)
            
            # Save the plot to a base64 encoded string
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            image_png = buffer.getvalue()
            buffer.close()
            
            chart = base64.b64encode(image_png).decode('utf-8')
            
            # Add to context
            context['performance_chart'] = chart
            context['responses'] = responses
        
        return context


class UserStatsView(LoginRequiredMixin, TemplateView):
    """
    View to display statistics and analytics for a user's quiz history.
    
    Requires authentication. Shows visualizations of the user's performance
    across different categories and over time.
    """
    template_name = 'quiz_app/user_stats.html'
    
    def get_context_data(self, **kwargs):
        """Add user statistics to the context."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get all completed quiz attempts by this user
        quiz_attempts = QuizAttempt.objects.filter(
            user=user,
            completed_at__isnull=False
        ).select_related('category')
        
        if quiz_attempts.exists():
            # Create a DataFrame for analysis
            data = {
                'date': [attempt.completed_at for attempt in quiz_attempts],
                'category': [attempt.category.name for attempt in quiz_attempts],
                'score_percentage': [attempt.score_percentage() for attempt in quiz_attempts],
                'total_questions': [attempt.total_questions for attempt in quiz_attempts]
            }
            df = pd.DataFrame(data)
            
            # 1. Performance over time chart
            plt.figure(figsize=(10, 5))
            sns.lineplot(data=df, x='date', y='score_percentage', hue='category', marker='o')
            plt.title('Quiz Performance Over Time')
            plt.xlabel('Date')
            plt.ylabel('Score (%)')
            plt.ylim(0, 100)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            time_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            
            # 2. Performance by category chart
            plt.figure(figsize=(8, 5))
            category_perf = df.groupby('category')['score_percentage'].mean().sort_values(ascending=False)
            sns.barplot(x=category_perf.index, y=category_perf.values)
            plt.title('Average Performance by Category')
            plt.xlabel('Category')
            plt.ylabel('Average Score (%)')
            plt.ylim(0, 100)
            plt.xticks(rotation=45)
            plt.tight_layout()
            
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight')
            buffer.seek(0)
            category_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            
            # Add charts to context
            context['time_chart'] = time_chart
            context['category_chart'] = category_chart
            
            # Add summary statistics
            context['total_quizzes'] = len(quiz_attempts)
            context['avg_score'] = df['score_percentage'].mean()
            context['categories_attempted'] = df['category'].nunique()
            context['best_category'] = category_perf.index[0] if not category_perf.empty else None
            
        return context 


class UserProfileView(LoginRequiredMixin, UpdateView):
    """
    View to display and update user profile information.
    
    This view handles both displaying the user's profile and updating it
    when the form is submitted. Requires the user to be logged in.
    """
    model = UserProfile
    template_name = 'quiz_app/user_profile.html'
    fields = ['bio', 'avatar', 'favorite_category', 'date_of_birth']
    success_url = reverse_lazy('quiz:profile')
    
    def get_object(self, queryset=None):
        """Return the current user's profile."""
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        """Add additional context data for the profile template."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get quiz statistics
        completed_quizzes = QuizAttempt.objects.filter(
            user=user,
            completed_at__isnull=False
        ).select_related('category')
        
        context.update({
            'completed_quizzes': completed_quizzes,
            'quiz_count': completed_quizzes.count(),
            'recent_quizzes': completed_quizzes[:5],  # Last 5 quizzes
        })
        
        return context


class RegisterView(CreateView):
    """
    View for user registration.
    
    This view handles the registration of new users, including form validation
    and user creation. On successful registration, it automatically creates a 
    UserProfile for the new user and redirects to the login page.
    """
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        # Create the user
        response = super().form_valid(form)
        user = self.object
        
        # Create UserProfile for the new user
        UserProfile.objects.create(user=user)
        
        # Add success message
        messages.success(
            self.request, 
            "Your account has been created successfully! You can now log in."
        )
        
        return response 