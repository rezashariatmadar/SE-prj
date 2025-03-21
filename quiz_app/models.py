"""
Models for the Quiz application.

This module defines the database models used in the quiz application:
- Category: Quiz categories/topics
- Question: Individual quiz questions
- Choice: Possible answers for a question
- QuizAttempt: Record of a user's quiz attempt
- QuizResponse: Individual answers within a quiz attempt
- UserProfile: Extended user information
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    """
    Represents a quiz category or topic.
    
    Categories are used to organize questions into logical groups,
    allowing users to select quizzes by topic of interest.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="The name of the quiz category"
    )
    description = models.TextField(
        blank=True,
        help_text="A detailed description of the category"
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text="CSS class for the category icon (e.g., 'fa-science')"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the category was created"
    )
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']
    
    def __str__(self):
        """String representation of the category."""
        return self.name
    
    def question_count(self):
        """Returns the number of questions in this category."""
        return self.question_set.count()


class Question(models.Model):
    """
    Represents a quiz question.
    
    Each question belongs to a category and has multiple choice answers.
    One of the choices must be marked as correct.
    """
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]
    
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text="The category this question belongs to"
    )
    text = models.TextField(
        help_text="The question text"
    )
    explanation = models.TextField(
        blank=True,
        help_text="Explanation of the correct answer (shown after answering)"
    )
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_CHOICES,
        default='medium',
        help_text="The difficulty level of this question"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the question was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the question was last updated"
    )
    
    class Meta:
        ordering = ['category', 'difficulty', 'created_at']
    
    def __str__(self):
        """String representation of the question."""
        return f"{self.text[:50]}..." if len(self.text) > 50 else self.text
    
    def correct_choice(self):
        """Returns the correct choice for this question."""
        try:
            return self.choice_set.get(is_correct=True)
        except (Choice.DoesNotExist, Choice.MultipleObjectsReturned):
            return None


class Choice(models.Model):
    """
    Represents a possible answer for a quiz question.
    
    Each Choice is linked to a Question, and one Choice per Question
    should be marked as correct (is_correct=True).
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        help_text="The question this choice belongs to"
    )
    text = models.CharField(
        max_length=255,
        help_text="The text of this answer choice"
    )
    is_correct = models.BooleanField(
        default=False,
        help_text="Whether this choice is the correct answer"
    )
    
    class Meta:
        ordering = ['question', 'pk']
    
    def __str__(self):
        """String representation of the choice."""
        return self.text
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure only one choice per question is marked correct.
        """
        if self.is_correct:
            # Set all other choices for this question to is_correct=False
            Choice.objects.filter(
                question=self.question, 
                is_correct=True
            ).update(is_correct=False)
        super().save(*args, **kwargs)


class QuizAttempt(models.Model):
    """
    Represents a user's attempt at a quiz.
    
    Records metadata about the quiz attempt, including when it was started,
    completed, which category was selected, and the overall score.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        help_text="The user who took the quiz (null for anonymous users)"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        help_text="The category of questions in this quiz"
    )
    started_at = models.DateTimeField(
        default=timezone.now,
        help_text="When the quiz attempt was started"
    )
    completed_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="When the quiz attempt was completed"
    )
    score = models.IntegerField(
        default=0,
        help_text="The total score achieved"
    )
    total_questions = models.IntegerField(
        default=0,
        help_text="The total number of questions in the quiz"
    )
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        """String representation of the quiz attempt."""
        username = self.user.username if self.user else "Anonymous"
        return f"{username}'s {self.category} quiz on {self.started_at.strftime('%Y-%m-%d')}"
    
    def is_complete(self):
        """Returns whether the quiz attempt has been completed."""
        return self.completed_at is not None
    
    def calculate_score(self):
        """
        Calculates and updates the score based on correct responses.
        
        Returns:
            int: The calculated score
        """
        correct_count = self.quizresponse_set.filter(
            is_correct=True
        ).count()
        
        self.score = correct_count
        self.save(update_fields=['score'])
        return self.score
    
    def score_percentage(self):
        """
        Returns the score as a percentage.
        
        Returns:
            float: Percentage score (0-100)
        """
        if self.total_questions == 0:
            return 0
        return (self.score / self.total_questions) * 100


class QuizResponse(models.Model):
    """
    Represents a user's response to a single question within a quiz attempt.
    
    Tracks which question was asked, which choice was selected, and whether
    the answer was correct.
    """
    quiz_attempt = models.ForeignKey(
        QuizAttempt,
        on_delete=models.CASCADE,
        help_text="The quiz attempt this response belongs to"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        help_text="The question that was answered"
    )
    selected_choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        help_text="The choice that was selected"
    )
    is_correct = models.BooleanField(
        default=False,
        help_text="Whether this response was correct"
    )
    response_time = models.DateTimeField(
        auto_now_add=True,
        help_text="When this question was answered"
    )
    
    class Meta:
        ordering = ['quiz_attempt', 'response_time']
        unique_together = ['quiz_attempt', 'question']
    
    def __str__(self):
        """String representation of the quiz response."""
        return f"Response to {self.question} in {self.quiz_attempt}"
    
    def save(self, *args, **kwargs):
        """
        Override save method to automatically set is_correct based on the selected choice.
        """
        # Determine if the selected choice is correct
        self.is_correct = self.selected_choice.is_correct
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """
    Extends the built-in User model with additional profile information.
    
    This model is connected to the User model with a one-to-one relationship
    and is automatically created/updated when the User model is saved.
    """
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='profile',
        help_text="The user this profile belongs to"
    )
    bio = models.TextField(
        blank=True,
        help_text="Short biography or description"
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        help_text="Profile picture"
    )
    favorite_category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User's favorite quiz category"
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
        help_text="User's date of birth"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the profile was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="When the profile was last updated"
    )
    
    def __str__(self):
        """String representation of the user profile."""
        return f"{self.user.username}'s Profile"
    
    def total_quizzes_taken(self):
        """Return the total number of quizzes completed by the user."""
        return self.user.quizattempt_set.filter(completed_at__isnull=False).count()
    
    def average_score(self):
        """Return the user's average score across all quizzes."""
        completed_quizzes = self.user.quizattempt_set.filter(completed_at__isnull=False)
        if completed_quizzes.exists():
            total_score = sum(quiz.score_percentage() for quiz in completed_quizzes)
            return total_score / completed_quizzes.count()
        return 0


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a UserProfile instance when a User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Update the UserProfile when the User is updated."""
    instance.profile.save() 