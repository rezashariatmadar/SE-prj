"""
Forms for the Quiz application.

This module defines the forms used in the quiz application for user input,
including quiz selection and customization.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Category, Question


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with extended fields.
    
    This form extends Django's UserCreationForm to include additional fields
    like email, first name, and last name for a more complete user profile.
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Required. Enter a valid email address."
    )
    first_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Optional. Enter your first name."
    )
    last_name = forms.CharField(
        max_length=30, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        help_text="Optional. Enter your last name."
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        # Add Bootstrap classes to all fields
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
            
    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


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
    
    time_limit = forms.ChoiceField(
        choices=[
            (0, 'No Time Limit'),
            (60, '1 Minute'),
            (120, '2 Minutes'),
            (300, '5 Minutes'),
            (600, '10 Minutes'),
            (900, '15 Minutes'),
            (1800, '30 Minutes'),
        ],
        initial=0,
        widget=forms.Select(attrs={'class': 'form-control'}),
        help_text="Choose a time limit for your quiz (optional)"
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
        
    def clean_time_limit(self):
        """
        Convert time_limit to an integer.
        """
        time_limit = self.cleaned_data.get('time_limit')
        return int(time_limit) 