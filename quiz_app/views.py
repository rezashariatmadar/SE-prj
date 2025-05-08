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
    
    Analytics Features:
    - Performance Over Time: Line chart tracking progress across different categories
    - Category Performance: Bar chart showing strengths and weaknesses by topic
    - Quiz Length Distribution: Pie chart showing quiz length patterns
    - Summary Statistics: Key metrics on quiz performance
    
    Implementation Notes:
    - Uses pandas for data organization and analysis
    - Uses matplotlib and seaborn for visualization creation
    - All charts are encoded as base64 for embedding in HTML
    """
    template_name = 'quiz_app/user_stats.html'
    
    def get_context_data(self, **kwargs):
        """
        Add user statistics to the context.
        
        This method:
        1. Retrieves the user's completed quiz attempts
        2. Processes the data using pandas DataFrame
        3. Generates three distinct visualization charts
        4. Calculates summary statistics
        5. Adds all data to the template context
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get all completed quiz attempts by this user
        quiz_attempts = QuizAttempt.objects.filter(
            user=user,
            completed_at__isnull=False
        ).select_related('category')
        
        if quiz_attempts.exists():
            # Create a DataFrame for analysis
            # This converts database records into a format suitable for data science processing
            data = {
                'date': [attempt.completed_at for attempt in quiz_attempts],
                'category': [attempt.category.name for attempt in quiz_attempts],
                'score_percentage': [attempt.score_percentage() for attempt in quiz_attempts],
                'total_questions': [attempt.total_questions for attempt in quiz_attempts]
            }
            df = pd.DataFrame(data)
            
            # Set the style for all charts - makes the charts visually consistent and attractive
            sns.set_style("whitegrid")
            plt.rcParams.update({
                'font.size': 12,
                'axes.labelsize': 14,
                'axes.titlesize': 16,
                'xtick.labelsize': 12,
                'ytick.labelsize': 12,
                'legend.fontsize': 12,
                'figure.titlesize': 18
            })
            
            # 1. Performance over time chart
            # This chart shows how scores change over time, helping users track their learning progress
            plt.figure(figsize=(12, 6))
            
            # Sort by date to ensure correct chronological order in the chart
            df = df.sort_values('date')
            
            # Create line plot - each line represents a different category
            ax = sns.lineplot(data=df, x='date', y='score_percentage', hue='category', marker='o', linewidth=2.5)
            
            # Improve plot styling
            plt.title('Quiz Performance Over Time', fontweight='bold', pad=20)
            plt.xlabel('Date', fontweight='bold')
            plt.ylabel('Score (%)', fontweight='bold')
            plt.ylim(0, 100)
            
            # Format x-axis dates nicely
            from matplotlib.dates import DateFormatter
            date_form = DateFormatter("%Y-%m-%d")
            ax.xaxis.set_major_formatter(date_form)
            
            # Rotate and align the tick labels for better readability
            plt.xticks(rotation=45, ha='right')
            
            # Add grid lines for better readability
            plt.grid(True, alpha=0.3)
            
            # Add legend with a title - explains what each line color represents
            plt.legend(title='Category', title_fontsize=12, loc='upper left', bbox_to_anchor=(1, 1))
            
            # Tight layout to prevent cutting off labels
            plt.tight_layout()
            
            # Save to buffer and encode as base64 for embedding in HTML
            # This allows the chart to be displayed without saving it as a separate file
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
            buffer.seek(0)
            time_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()
            
            # 2. Performance by category chart
            # This bar chart helps users identify their strengths and weaknesses across topics
            plt.figure(figsize=(10, 6))
            
            # Calculate average scores by category and sort from highest to lowest
            if not df.empty:
                category_perf = df.groupby('category')['score_percentage'].mean().sort_values(ascending=False)
                
                # Create bar chart with better styling
                ax = sns.barplot(x=category_perf.index, y=category_perf.values, palette='viridis')
                
                # Add value labels on top of each bar for precise score information
                for i, v in enumerate(category_perf.values):
                    ax.text(i, v + 2, f"{v:.1f}%", ha='center', fontweight='bold')
                
                # Improve styling
                plt.title('Average Performance by Category', fontweight='bold', pad=20)
                plt.xlabel('Category', fontweight='bold')
                plt.ylabel('Average Score (%)', fontweight='bold')
                plt.ylim(0, 105)  # Extended to fit value labels
                
                # Ensure x labels are visible
                plt.xticks(rotation=45, ha='right')
                
                # Add a horizontal line for the overall average as a reference point
                overall_avg = df['score_percentage'].mean()
                plt.axhline(y=overall_avg, color='red', linestyle='--', label=f'Overall Avg: {overall_avg:.1f}%')
                plt.legend()
                
                # Add grid lines for better readability
                plt.grid(True, axis='y', alpha=0.3)
                
                # Ensure everything fits
                plt.tight_layout()
                
                # Save to buffer and encode as base64 for HTML embedding
                buffer = BytesIO()
                plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
                buffer.seek(0)
                category_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
                buffer.close()
                plt.close()
                
                context['category_chart'] = category_chart
            
            # 3. Question distribution chart (pie chart)
            # This chart shows what quiz lengths the user tends to select
            plt.figure(figsize=(8, 6))
            
            # Count quizzes by total questions
            question_counts = df['total_questions'].value_counts().sort_index()
            
            # Create pie chart with percentage labels
            plt.pie(question_counts, labels=[f"{count} questions" for count in question_counts.index], 
                    autopct='%1.1f%%', startangle=90, shadow=True, 
                    wedgeprops={'linewidth': 1, 'edgecolor': 'white'},
                    textprops={'fontsize': 12, 'fontweight': 'bold'})
            
            plt.title('Quiz Length Distribution', fontweight='bold', pad=20)
            plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
            
            # Save to buffer and encode for HTML embedding
            buffer = BytesIO()
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
            buffer.seek(0)
            question_dist_chart = base64.b64encode(buffer.getvalue()).decode('utf-8')
            buffer.close()
            plt.close()
            
            # Add charts to context for use in the template
            context['time_chart'] = time_chart
            context['question_dist_chart'] = question_dist_chart
            
            # Add summary statistics - these provide an overall picture of performance
            context['total_quizzes'] = len(quiz_attempts)
            context['avg_score'] = df['score_percentage'].mean()
            context['categories_attempted'] = df['category'].nunique()
            context['best_category'] = category_perf.index[0] if not category_perf.empty else None
            context['highest_score'] = df['score_percentage'].max()
            context['lowest_score'] = df['score_percentage'].min()
            context['perfect_score_count'] = len(df[df['score_percentage'] == 100])
            
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