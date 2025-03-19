"""
Admin configuration for the Quiz application.

This module registers the quiz application models with Django's admin site
and customizes their admin interfaces for better usability.
"""

from django.contrib import admin
from .models import Category, Question, Choice, QuizAttempt, QuizResponse


class ChoiceInline(admin.TabularInline):
    """
    Inline admin interface for choices.
    
    Allows editing choices directly within the question admin page.
    """
    model = Choice
    extra = 4  # Show 4 empty choice forms by default
    fields = ['text', 'is_correct']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin interface for the Question model.
    
    Includes filters, search fields, and inline choices editing.
    """
    list_display = ['text_short', 'category', 'difficulty', 'created_at']
    list_filter = ['category', 'difficulty', 'created_at']
    search_fields = ['text', 'explanation']
    inlines = [ChoiceInline]
    date_hierarchy = 'created_at'
    
    def text_short(self, obj):
        """Return a shortened version of the question text for list display."""
        max_length = 50
        return (obj.text[:max_length] + '...') if len(obj.text) > max_length else obj.text
    text_short.short_description = 'Question'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin interface for the Category model.
    """
    list_display = ['name', 'question_count', 'created_at']
    search_fields = ['name', 'description']
    date_hierarchy = 'created_at'


class QuizResponseInline(admin.TabularInline):
    """
    Inline admin interface for quiz responses.
    
    Shows responses within the quiz attempt admin page.
    """
    model = QuizResponse
    extra = 0  # Don't show any empty forms
    fields = ['question', 'selected_choice', 'is_correct']
    readonly_fields = ['question', 'selected_choice', 'is_correct']
    can_delete = False


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """
    Admin interface for the QuizAttempt model.
    """
    list_display = ['id', 'user_display', 'category', 'score', 'total_questions', 'score_percentage', 'started_at', 'is_complete']
    list_filter = ['category', 'started_at', 'completed_at']
    search_fields = ['user__username', 'category__name']
    date_hierarchy = 'started_at'
    inlines = [QuizResponseInline]
    
    def user_display(self, obj):
        """Return the username or 'Anonymous' if no user."""
        return obj.user.username if obj.user else 'Anonymous'
    user_display.short_description = 'User'
    
    def score_percentage(self, obj):
        """Return the score as a percentage."""
        percentage = obj.score_percentage()
        return f"{percentage:.1f}%"
    score_percentage.short_description = 'Score %'
    
    def is_complete(self, obj):
        """Return whether the quiz attempt is complete."""
        return obj.completed_at is not None
    is_complete.boolean = True
    is_complete.short_description = 'Complete'


@admin.register(QuizResponse)
class QuizResponseAdmin(admin.ModelAdmin):
    """
    Admin interface for the QuizResponse model.
    """
    list_display = ['quiz_attempt', 'question_short', 'selected_choice_short', 'is_correct', 'response_time']
    list_filter = ['is_correct', 'response_time', 'quiz_attempt__category']
    search_fields = ['question__text', 'selected_choice__text']
    date_hierarchy = 'response_time'
    
    def question_short(self, obj):
        """Return a shortened version of the question text."""
        max_length = 30
        return (obj.question.text[:max_length] + '...') if len(obj.question.text) > max_length else obj.question.text
    question_short.short_description = 'Question'
    
    def selected_choice_short(self, obj):
        """Return a shortened version of the selected choice text."""
        max_length = 30
        return (obj.selected_choice.text[:max_length] + '...') if len(obj.selected_choice.text) > max_length else obj.selected_choice.text
    selected_choice_short.short_description = 'Selected Choice' 