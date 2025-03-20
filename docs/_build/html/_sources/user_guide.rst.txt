User Guide
==========

This guide provides detailed instructions on how to use the Quiz Game application,
from taking quizzes to viewing statistics and managing your account.

Getting Started
--------------

Accessing the Application
~~~~~~~~~~~~~~~~~~~~~~~

Open your web browser and navigate to the Quiz Game URL:

* If running locally: http://127.0.0.1:8000/
* If deployed: https://your-quiz-game-domain.com/

The homepage displays a welcome message and available quiz categories.

.. image:: _static/homepage_screenshot.png
   :alt: Homepage Screenshot
   :align: center
   :width: 600px

Navigation
~~~~~~~~~

The main navigation menu provides access to these key areas:

* **Home**: Return to the welcome page
* **Categories**: Browse all quiz categories
* **My Stats**: View your quiz statistics (authenticated users only)
* **Login/Logout**: Manage your session

Taking a Quiz
------------

Starting a Quiz
~~~~~~~~~~~~~

1. On the homepage, you'll see a "Start a New Quiz" card
2. Select a category from the dropdown menu
3. Choose the number of questions (5-20)
4. Click the "Start Quiz" button

.. image:: _static/start_quiz_screenshot.png
   :alt: Start Quiz Form
   :align: center
   :width: 500px

Answering Questions
~~~~~~~~~~~~~~~~~

For each question:

1. Read the question carefully
2. Select your answer by clicking one of the options
3. Click "Next Question" to proceed

.. note::
   You cannot go back to previous questions once submitted.

.. image:: _static/question_screenshot.png
   :alt: Question Screenshot
   :align: center
   :width: 600px

**Navigation Keys**:

* You can use number keys (1-4) to select answers
* Press Enter to submit and go to the next question

Progress Tracking
~~~~~~~~~~~~~~~

While taking a quiz:

* The progress bar at the top shows your advancement
* The question number indicator shows your current position (e.g., "Question 3 of 10")
* The category name is displayed for reference

Viewing Results
--------------

Score Summary
~~~~~~~~~~~

After completing a quiz, you'll see your results:

1. **Score**: Number of correct answers and percentage
2. **Progress Bar**: Visual representation of your score
3. **Feedback Message**: Encouragement based on your performance

.. image:: _static/results_screenshot.png
   :alt: Results Screenshot
   :align: center
   :width: 600px

Performance Analysis
~~~~~~~~~~~~~~~~~~

The results page includes:

* **Performance by Difficulty Chart**: Bar chart showing how well you did on easy, medium, and hard questions
* **Question Review**: List of all questions with your answers, correct answers, and explanations

Actions from Results Page
~~~~~~~~~~~~~~~~~~~~~~

From the results page, you can:

* **Try Again**: Take another quiz in the same category
* **Back to Home**: Return to the homepage to select a different category

User Statistics
--------------

.. note::
   The statistics features are only available to registered and authenticated users.

Accessing Statistics
~~~~~~~~~~~~~~~~~~

Click "My Stats" in the navigation menu to view your quiz history and performance analytics.

Available Statistics
~~~~~~~~~~~~~~~~~~

The statistics dashboard includes:

1. **Performance Over Time**:
   
   * Line chart showing scores across multiple quiz attempts
   * Color-coded by category
   * Tracks your learning progress

2. **Performance by Category**:
   
   * Bar chart comparing your average scores across different categories
   * Helps identify your strengths and areas for improvement

3. **Summary Statistics**:
   
   * Total quizzes completed
   * Average score percentage
   * Number of categories attempted
   * Your best-performing category

.. image:: _static/stats_screenshot.png
   :alt: Statistics Screenshot
   :align: center
   :width: 600px

Account Management
-----------------

Registration
~~~~~~~~~~

To create an account:

1. Click "Login" in the navigation menu
2. Click "Register" on the login page
3. Fill in the required information:
   * Username
   * Email address
   * Password (entered twice for confirmation)
4. Click "Register" to create your account

Login
~~~~~

To log into your account:

1. Click "Login" in the navigation menu
2. Enter your username and password
3. Click "Login"

.. tip::
   Check "Remember me" to stay logged in on your device.

Logout
~~~~~~

To log out:

1. Click "Logout" in the navigation menu
2. You will be redirected to the homepage

Password Reset
~~~~~~~~~~~~

If you forget your password:

1. Click "Login" in the navigation menu
2. Click "Forgot Password?"
3. Enter your email address
4. Check your email for a password reset link
5. Follow the link to set a new password

Tips for Success
--------------

Quiz Strategies
~~~~~~~~~~~~~

* **Read carefully**: Take your time to understand each question
* **Process of elimination**: If unsure, try to eliminate obviously wrong answers
* **Look for clues**: Sometimes parts of the question hint at the answer
* **Don't overthink**: Often your first instinct is correct

Learning from Results
~~~~~~~~~~~~~~~~~~~

* **Review explanations**: Read the explanations for both correct and incorrect answers
* **Focus on weak areas**: Pay attention to categories or difficulty levels where you scored lower
* **Retake quizzes**: Try the same category again to reinforce learning
* **Track progress**: Watch your performance improve over time in the statistics

Mobile Usage
----------

The Quiz Game application is fully responsive and can be used on:

* Desktop computers
* Tablets
* Smartphones

The interface automatically adapts to your screen size for optimal experience.

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~

**Problem**: Quiz doesn't start after selecting a category
**Solution**: Make sure the category has questions available. Try a different category.

**Problem**: Session expired during a quiz
**Solution**: Log in again and start a new quiz.

**Problem**: Charts not displaying in statistics
**Solution**: Make sure your browser supports HTML5 and has JavaScript enabled.

Getting Help
~~~~~~~~~~

If you encounter any issues:

* Check the FAQ section
* Contact support via email: support@quizgame.example
* Visit the help forum 