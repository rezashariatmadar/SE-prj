"""
Forms for the Quiz application.

This module defines the forms used in the quiz application for user input,
including quiz selection and customization.
"""

from django import forms
from .models import Category, Question


class QuizSelectionForm(forms.Form):
    """
    Form for selecting a quiz category and number of questions.
    
    This form allows users to choose which category of questions they want
    to be quizzed on and how many questions they want in their quiz.
    """
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose the topic you want to be quizzed on"
    )
    
    num_questions = forms.IntegerField(
        min_value=5,
        max_value=20,
        initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'min': '5',
            'max': '20',
            'step': '1'
        }),
        help_text="Choose how many questions you want (5-20)"
    )
    
    def __init__(self, *args, **kwargs):
        """Initialize the form with only categories that have questions."""
        super().__init__(*args, **kwargs)
        # Get categories that have at least one question
        self.fields['category'].queryset = Category.objects.filter(
            question__isnull=False
        ).distinct()
    
    def clean(self):
        """Validate the form data."""
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        num_questions = cleaned_data.get('num_questions')
        
        if not category:
            self.add_error('category', 'Please select a category')
            
        if num_questions is None:
            self.add_error('num_questions', 'Please specify the number of questions')
        elif num_questions < 5:
            self.add_error('num_questions', 'Number of questions must be at least 5')
        elif num_questions > 20:
            self.add_error('num_questions', 'Number of questions must not exceed 20')
            
        return cleaned_data
    
    def clean_num_questions(self):
        """
        Validate that the number of questions doesn't exceed available questions.
        """
        category = self.cleaned_data.get('category')
        num_questions = self.cleaned_data.get('num_questions')
        
        if category and num_questions:
            available_questions = Question.objects.filter(category=category).count()
            if num_questions > available_questions:
                raise forms.ValidationError(
                    f"Only {available_questions} questions available in this category. "
                    f"Please select a lower number."
                )
        
        return num_questions 