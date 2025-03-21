"""
URL Configuration for quiz_app.

This module defines the URL patterns specific to the quiz application.
Each URL pattern is associated with a view that handles the corresponding request.
"""

from django.urls import path
from . import views

app_name = 'quiz'  # Application namespace for URL naming

urlpatterns = [
    # Home page / index view
    path('', views.IndexView.as_view(), name='index'),
    
    # List of quiz categories
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    
    # Start a new quiz
    path('start/', views.QuizStartView.as_view(), name='start'),
    
    # Answer quiz questions
    path('question/', views.QuestionView.as_view(), name='question'),
    
    # View quiz results
    path('results/<int:quiz_id>/', views.ResultsView.as_view(), name='results'),
    
    # User statistics dashboard
    path('stats/', views.UserStatsView.as_view(), name='user_stats'),
    
    # User profile page
    path('profile/', views.UserProfileView.as_view(), name='profile'),
] 