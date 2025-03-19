=====
Forms
=====

This document details the form classes used in the Quiz Application, explaining their structure, validation logic, and usage.

QuizSelectionForm
----------------

The ``QuizSelectionForm`` is used to start a new quiz. It allows users to select a category and specify how many questions they want to answer.

.. code-block:: python

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

Field Specifications
~~~~~~~~~~~~~~~~~~~

**category**
    A dropdown field that allows users to select a quiz category.
    
    * **Type**: ``ModelChoiceField``
    * **Queryset**: All ``Category`` objects
    * **Widget**: Select with Bootstrap styling
    * **Help Text**: "Choose the topic you want to be quizzed on"

**num_questions**
    A number input field that allows users to specify how many questions they want in their quiz.
    
    * **Type**: ``IntegerField``
    * **Constraints**: Minimum 5, Maximum 20
    * **Default Value**: 10
    * **Widget**: NumberInput with Bootstrap styling and HTML5 attributes
    * **Help Text**: "Choose how many questions you want (5-20)"

Initialization
~~~~~~~~~~~~~

The form's ``__init__`` method customizes the category queryset to only include categories that have questions:

.. code-block:: python

    def __init__(self, *args, **kwargs):
        """Initialize the form with only categories that have questions."""
        super().__init__(*args, **kwargs)
        # Get categories that have at least one question
        self.fields['category'].queryset = Category.objects.filter(
            question__isnull=False
        ).distinct()

This ensures that users can only select categories that have at least one question, preventing them from starting quizzes with empty categories.

Validation Logic
~~~~~~~~~~~~~~

The form implements comprehensive validation logic to ensure that user input is valid:

1. **Basic Form Validation**

   The ``clean`` method validates the overall form data:

   .. code-block:: python

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

2. **Field-Specific Validation**

   The ``clean_num_questions`` method implements additional validation for the number of questions field:

   .. code-block:: python

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

   This method ensures that users cannot select more questions than are available in the chosen category.

Usage in Templates
~~~~~~~~~~~~~~~~

The form is typically used in the ``index.html`` template:

.. code-block:: html

    <form method="post" action="{% url 'quiz:start' %}" id="quiz-form">
        {% csrf_token %}
        <div class="form-group mb-3">
            <label for="{{ form.category.id_for_label }}">
                <i class="fas fa-folder me-2"></i>{{ form.category.label|default:"Category" }}
            </label>
            {{ form.category }}
            {% if form.category.errors %}
                <div class="text-danger mt-1">
                    {{ form.category.errors }}
                </div>
            {% endif %}
            <small class="form-text text-muted">{{ form.category.help_text }}</small>
        </div>
        <div class="form-group mb-3">
            <label for="{{ form.num_questions.id_for_label }}">
                <i class="fas fa-question-circle me-2"></i>{{ form.num_questions.label|default:"Number of Questions" }}
            </label>
            {{ form.num_questions }}
            {% if form.num_questions.errors %}
                <div class="text-danger mt-1">
                    {{ form.num_questions.errors }}
                </div>
            {% endif %}
            <small class="form-text text-muted">{{ form.num_questions.help_text }}</small>
        </div>
        <div class="d-grid">
            <button type="submit" class="btn btn-primary btn-lg">
                <i class="fas fa-play me-2"></i>Start Quiz
            </button>
        </div>
        {% if form.non_field_errors %}
            <div class="alert alert-danger mt-3">
                {{ form.non_field_errors }}
            </div>
        {% endif %}
    </form>

JavaScript Validation
~~~~~~~~~~~~~~~~~~~

In addition to server-side validation, client-side validation is implemented using JavaScript:

.. code-block:: javascript

    $("#quiz-form").on('submit', function(e) {
        var category = $("#{{ form.category.id_for_label }}").val();
        var numQuestions = $("#{{ form.num_questions.id_for_label }}").val();
        var isValid = true;
        
        // Reset error messages
        $(".text-danger").remove();
        
        // Validate category
        if (!category) {
            $("#{{ form.category.id_for_label }}").after('<div class="text-danger mt-1">Please select a category</div>');
            isValid = false;
        }
        
        // Validate number of questions
        if (!numQuestions) {
            $("#{{ form.num_questions.id_for_label }}").after('<div class="text-danger mt-1">Please enter the number of questions</div>');
            isValid = false;
        } else {
            var num = parseInt(numQuestions);
            if (isNaN(num) || num < 5 || num > 20) {
                $("#{{ form.num_questions.id_for_label }}").after('<div class="text-danger mt-1">Number must be between 5 and 20</div>');
                isValid = false;
            }
        }
        
        return isValid;
    });

This JavaScript validation provides immediate feedback to users, enhancing the overall user experience.

Integration with Views
~~~~~~~~~~~~~~~~~~~~

The form is processed in the ``QuizStartView``:

.. code-block:: python

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
                
                # Create a new quiz attempt
                quiz_attempt = QuizAttempt(
                    user=request.user if request.user.is_authenticated else None,
                    category=category,
                    total_questions=num_questions
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

When the form is valid, the view creates a new quiz attempt, selects random questions, and redirects to the question page. When the form is invalid, it renders the index page with error messages.

Testing
~~~~~~

The form's validation logic is thoroughly tested in the test suite:

.. code-block:: python

    def test_quiz_selection_form_valid_data(self):
        """Test the form with valid data across the allowed range (5-20 questions)."""
        # Test minimum number of questions (5)
        form_data = {
            'category': self.category.id,
            'num_questions': 5
        }
        form = QuizSelectionForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors for 5 questions: {form.errors}")
        
        # Test middle range (10 questions)
        form_data['num_questions'] = 10
        form = QuizSelectionForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors for 10 questions: {form.errors}")
        
        # Test maximum number of questions (20)
        form_data['num_questions'] = 20
        form = QuizSelectionForm(data=form_data)
        self.assertTrue(form.is_valid(), f"Form errors for 20 questions: {form.errors}")

Tests are implemented for valid inputs, invalid inputs, edge cases, and error handling.

Conclusion
---------

The ``QuizSelectionForm`` plays a vital role in the Quiz Application, providing a user-friendly interface for starting new quizzes. Its comprehensive validation logic ensures that users can only select valid options, enhancing the overall user experience and preventing errors during quiz creation. 