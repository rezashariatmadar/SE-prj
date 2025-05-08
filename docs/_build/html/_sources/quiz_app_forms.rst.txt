Forms
=====

Last updated: 2025-05-08

This document describes all forms in the quiz_app application.


QuizSelectionForm
-----------------

Form for selecting a quiz category and number of questions.

This form allows users to choose which category of questions they want
to be quizzed on and how many questions they want in their quiz.


Fields
~~~~~~


category
    Type: ModelChoiceField
    Required: True
    Description: Choose the topic you want to be quizzed on

num_questions
    Type: IntegerField
    Required: True
    Description: Choose how many questions you want (5-20)

time_limit
    Type: ChoiceField
    Required: True
    Description: Choose a time limit for your quiz (optional)

UserCreationForm
----------------

A form that creates a user, with no privileges, from the given username and
password.


Fields
~~~~~~


password1
    Type: CharField
    Required: True
    Description: <ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>

password2
    Type: CharField
    Required: True
    Description: Enter the same password as before, for verification.

UserRegistrationForm
--------------------

Form for user registration with extended fields.

This form extends Django's UserCreationForm to include additional fields
like email, first name, and last name for a more complete user profile.


Fields
~~~~~~


password1
    Type: CharField
    Required: True
    Description: <ul><li>Your password can’t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can’t be a commonly used password.</li><li>Your password can’t be entirely numeric.</li></ul>

password2
    Type: CharField
    Required: True
    Description: Enter the same password as before, for verification.

email
    Type: EmailField
    Required: True
    Description: Required. Enter a valid email address.

first_name
    Type: CharField
    Required: False
    Description: Optional. Enter your first name.

last_name
    Type: CharField
    Required: False
    Description: Optional. Enter your last name.
