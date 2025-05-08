Views
=====

Last updated: 2025-05-08

This document describes all views in the quiz_app application.


CategoryListView
----------------

View to display all available quiz categories.


Template
~~~~~~~~
quiz_app/category_list.html

CreateView
----------

View for creating a new object, with a response rendered by a template.


Template
~~~~~~~~
None

DetailView
----------

Render a "detail" view of an object.

By default this is a model instance looked up from `self.queryset`, but the
view will support display of *any* object by overriding `self.get_object()`.


Template
~~~~~~~~
None

IndexView
---------

View for the home page of the quiz application.

Displays a welcome message and available quiz categories.


Template
~~~~~~~~
quiz_app/index.html

ListView
--------

Render some list of objects, set by `self.model` or `self.queryset`.
`self.queryset` can actually be any iterable of items, not just a queryset.


Template
~~~~~~~~
None

QuestionView
------------

View to display a quiz question and process the answer.


Template
~~~~~~~~
quiz_app/question.html

QuizStartView
-------------

View to handle the start of a new quiz.

Creates a new QuizAttempt and redirects to the first question.


RegisterView
------------

View for user registration.

This view handles the registration of new users, including form validation
and user creation. On successful registration, it automatically creates a 
UserProfile for the new user and redirects to the login page.


Template
~~~~~~~~
registration/register.html

ResultsView
-----------

View to display the results of a completed quiz.


Template
~~~~~~~~
quiz_app/results.html

TemplateView
------------

Render a template. Pass keyword arguments from the URLconf to the context.


Template
~~~~~~~~
None

UpdateView
----------

View for updating an object, with a response rendered by a template.


Template
~~~~~~~~
None

UserProfileView
---------------

View to display and update user profile information.

This view handles both displaying the user's profile and updating it
when the form is submitted. Requires the user to be logged in.


Template
~~~~~~~~
quiz_app/user_profile.html

UserStatsView
-------------

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


Template
~~~~~~~~
quiz_app/user_stats.html

View
----

Intentionally simple parent class for all views. Only implements
dispatch-by-method and simple sanity checking.

