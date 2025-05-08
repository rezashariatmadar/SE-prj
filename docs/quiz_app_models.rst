Models
======

Last updated: 2025-05-08

This document describes all models in the quiz_app application.


Category
--------

Represents a quiz category or topic.

Categories are used to organize questions into logical groups,
allowing users to select quizzes by topic of interest.

Fields
~~~~~~


question
    Type: ForeignKey
    Description: No description available

quizattempt
    Type: ForeignKey
    Description: No description available

userprofile
    Type: ForeignKey
    Description: No description available

id
    Type: BigAutoField
    Description: 

name
    Type: CharField
    Description: The name of the quiz category

description
    Type: TextField
    Description: A detailed description of the category

icon
    Type: CharField
    Description: CSS class for the category icon (e.g., 'fa-science')

created_at
    Type: DateTimeField
    Description: When the category was created

Methods
~~~~~~~

adelete
    No documentation available.

arefresh_from_db
    No documentation available.

asave
    No documentation available.

clean
    Hook for doing any extra model-wide validation after clean() has been
called on every field by self.clean_fields. Any ValidationError raised
by this method will not be associated with a particular field; it will
have a special-case association with the field defined by NON_FIELD_ERRORS.

clean_fields
    Clean all fields and raise a ValidationError containing a dict
of all validation errors if any occur.

date_error_message
    No documentation available.

delete
    No documentation available.

full_clean
    Call clean_fields(), clean(), validate_unique(), and
validate_constraints() on the model. Raise a ValidationError for any
errors that occur.

get_constraints
    No documentation available.

get_deferred_fields
    Return a set containing names of deferred fields for this instance.

get_next_by_created_at
    No documentation available.

get_previous_by_created_at
    No documentation available.

prepare_database_save
    No documentation available.

question_count
    Returns the number of questions in this category.

refresh_from_db
    Reload field values from the database.

By default, the reloading happens from the database this instance was
loaded from, or by the read router if this instance wasn't loaded from
any database. The using parameter will override the default.

Fields can be used to specify which fields to reload. The fields
should be an iterable of field attnames. If fields is None, then
all non-deferred fields are reloaded.

When accessing deferred fields of an instance, the deferred loading
of the field will call this method.

save
    Save the current instance. Override this in a subclass if you want to
control the saving process.

The 'force_insert' and 'force_update' parameters can be used to insist
that the "save" must be an SQL insert or update (or equivalent for
non-SQL backends), respectively. Normally, they should not be set.

save_base
    Handle the parts of saving which should be done only once per save,
yet need to be done in raw saves, too. This includes some sanity
checks and signal sending.

The 'raw' argument is telling save_base not to save any parent
models and not to do any changes to the values before save. This
is used by fixture loading.

serializable_value
    Return the value of the field name for this instance. If the field is
a foreign key, return the id value instead of the object. If there's
no Field object with this name on the model, return the model
attribute's value.

Used to serialize a field's value (in the serializer, or form output,
for example). Normally, you would just access the attribute directly
and not use this method.

unique_error_message
    No documentation available.

validate_constraints
    No documentation available.

validate_unique
    Check unique constraints on the model and raise ValidationError if any
failed.

Question
--------

Represents a quiz question.

Each question belongs to a category and has multiple choice answers.
One of the choices must be marked as correct.

Fields
~~~~~~


choice
    Type: ForeignKey
    Description: No description available

quizresponse
    Type: ForeignKey
    Description: No description available

id
    Type: BigAutoField
    Description: 

category
    Type: ForeignKey
    Description: The category this question belongs to

text
    Type: TextField
    Description: The question text

explanation
    Type: TextField
    Description: Explanation of the correct answer (shown after answering)

difficulty
    Type: CharField
    Description: The difficulty level of this question

created_at
    Type: DateTimeField
    Description: When the question was created

updated_at
    Type: DateTimeField
    Description: When the question was last updated

Methods
~~~~~~~

adelete
    No documentation available.

arefresh_from_db
    No documentation available.

asave
    No documentation available.

clean
    Hook for doing any extra model-wide validation after clean() has been
called on every field by self.clean_fields. Any ValidationError raised
by this method will not be associated with a particular field; it will
have a special-case association with the field defined by NON_FIELD_ERRORS.

clean_fields
    Clean all fields and raise a ValidationError containing a dict
of all validation errors if any occur.

correct_choice
    Returns the correct choice for this question.

date_error_message
    No documentation available.

delete
    No documentation available.

full_clean
    Call clean_fields(), clean(), validate_unique(), and
validate_constraints() on the model. Raise a ValidationError for any
errors that occur.

get_constraints
    No documentation available.

get_deferred_fields
    Return a set containing names of deferred fields for this instance.

get_difficulty_display
    No documentation available.

get_next_by_created_at
    No documentation available.

get_next_by_updated_at
    No documentation available.

get_previous_by_created_at
    No documentation available.

get_previous_by_updated_at
    No documentation available.

prepare_database_save
    No documentation available.

refresh_from_db
    Reload field values from the database.

By default, the reloading happens from the database this instance was
loaded from, or by the read router if this instance wasn't loaded from
any database. The using parameter will override the default.

Fields can be used to specify which fields to reload. The fields
should be an iterable of field attnames. If fields is None, then
all non-deferred fields are reloaded.

When accessing deferred fields of an instance, the deferred loading
of the field will call this method.

save
    Save the current instance. Override this in a subclass if you want to
control the saving process.

The 'force_insert' and 'force_update' parameters can be used to insist
that the "save" must be an SQL insert or update (or equivalent for
non-SQL backends), respectively. Normally, they should not be set.

save_base
    Handle the parts of saving which should be done only once per save,
yet need to be done in raw saves, too. This includes some sanity
checks and signal sending.

The 'raw' argument is telling save_base not to save any parent
models and not to do any changes to the values before save. This
is used by fixture loading.

serializable_value
    Return the value of the field name for this instance. If the field is
a foreign key, return the id value instead of the object. If there's
no Field object with this name on the model, return the model
attribute's value.

Used to serialize a field's value (in the serializer, or form output,
for example). Normally, you would just access the attribute directly
and not use this method.

unique_error_message
    No documentation available.

validate_constraints
    No documentation available.

validate_unique
    Check unique constraints on the model and raise ValidationError if any
failed.

Choice
------

Represents a possible answer for a quiz question.

Each Choice is linked to a Question, and one Choice per Question
should be marked as correct (is_correct=True).

Fields
~~~~~~


quizresponse
    Type: ForeignKey
    Description: No description available

id
    Type: BigAutoField
    Description: 

question
    Type: ForeignKey
    Description: The question this choice belongs to

text
    Type: CharField
    Description: The text of this answer choice

is_correct
    Type: BooleanField
    Description: Whether this choice is the correct answer

Methods
~~~~~~~

adelete
    No documentation available.

arefresh_from_db
    No documentation available.

asave
    No documentation available.

clean
    Hook for doing any extra model-wide validation after clean() has been
called on every field by self.clean_fields. Any ValidationError raised
by this method will not be associated with a particular field; it will
have a special-case association with the field defined by NON_FIELD_ERRORS.

clean_fields
    Clean all fields and raise a ValidationError containing a dict
of all validation errors if any occur.

date_error_message
    No documentation available.

delete
    No documentation available.

full_clean
    Call clean_fields(), clean(), validate_unique(), and
validate_constraints() on the model. Raise a ValidationError for any
errors that occur.

get_constraints
    No documentation available.

get_deferred_fields
    Return a set containing names of deferred fields for this instance.

prepare_database_save
    No documentation available.

refresh_from_db
    Reload field values from the database.

By default, the reloading happens from the database this instance was
loaded from, or by the read router if this instance wasn't loaded from
any database. The using parameter will override the default.

Fields can be used to specify which fields to reload. The fields
should be an iterable of field attnames. If fields is None, then
all non-deferred fields are reloaded.

When accessing deferred fields of an instance, the deferred loading
of the field will call this method.

save
    Override save method to ensure only one choice per question is marked correct.

save_base
    Handle the parts of saving which should be done only once per save,
yet need to be done in raw saves, too. This includes some sanity
checks and signal sending.

The 'raw' argument is telling save_base not to save any parent
models and not to do any changes to the values before save. This
is used by fixture loading.

serializable_value
    Return the value of the field name for this instance. If the field is
a foreign key, return the id value instead of the object. If there's
no Field object with this name on the model, return the model
attribute's value.

Used to serialize a field's value (in the serializer, or form output,
for example). Normally, you would just access the attribute directly
and not use this method.

unique_error_message
    No documentation available.

validate_constraints
    No documentation available.

validate_unique
    Check unique constraints on the model and raise ValidationError if any
failed.

QuizAttempt
-----------

Represents a user's attempt at a quiz.

Records metadata about the quiz attempt, including when it was started,
completed, which category was selected, and the overall score.

Fields
~~~~~~


quizresponse
    Type: ForeignKey
    Description: No description available

id
    Type: BigAutoField
    Description: 

user
    Type: ForeignKey
    Description: The user who took the quiz (null for anonymous users)

category
    Type: ForeignKey
    Description: The category of questions in this quiz

started_at
    Type: DateTimeField
    Description: When the quiz attempt was started

completed_at
    Type: DateTimeField
    Description: When the quiz attempt was completed

score
    Type: IntegerField
    Description: The total score achieved

total_questions
    Type: IntegerField
    Description: The total number of questions in the quiz

time_limit
    Type: IntegerField
    Description: Time limit for the quiz in seconds (0 means no limit)

Methods
~~~~~~~

adelete
    No documentation available.

arefresh_from_db
    No documentation available.

asave
    No documentation available.

calculate_score
    Calculates and updates the score based on correct responses.


Returns
~~~~~~~~
    int: The calculated score

clean
    Hook for doing any extra model-wide validation after clean() has been
called on every field by self.clean_fields. Any ValidationError raised
by this method will not be associated with a particular field; it will
have a special-case association with the field defined by NON_FIELD_ERRORS.

clean_fields
    Clean all fields and raise a ValidationError containing a dict
of all validation errors if any occur.

date_error_message
    No documentation available.

delete
    No documentation available.

full_clean
    Call clean_fields(), clean(), validate_unique(), and
validate_constraints() on the model. Raise a ValidationError for any
errors that occur.

get_constraints
    No documentation available.

get_deferred_fields
    Return a set containing names of deferred fields for this instance.

get_next_by_started_at
    No documentation available.

get_previous_by_started_at
    No documentation available.

is_complete
    Returns whether the quiz attempt has been completed.

prepare_database_save
    No documentation available.

refresh_from_db
    Reload field values from the database.

By default, the reloading happens from the database this instance was
loaded from, or by the read router if this instance wasn't loaded from
any database. The using parameter will override the default.

Fields can be used to specify which fields to reload. The fields
should be an iterable of field attnames. If fields is None, then
all non-deferred fields are reloaded.

When accessing deferred fields of an instance, the deferred loading
of the field will call this method.

save
    Save the current instance. Override this in a subclass if you want to
control the saving process.

The 'force_insert' and 'force_update' parameters can be used to insist
that the "save" must be an SQL insert or update (or equivalent for
non-SQL backends), respectively. Normally, they should not be set.

save_base
    Handle the parts of saving which should be done only once per save,
yet need to be done in raw saves, too. This includes some sanity
checks and signal sending.

The 'raw' argument is telling save_base not to save any parent
models and not to do any changes to the values before save. This
is used by fixture loading.

score_percentage
    Returns the score as a percentage.


Returns
~~~~~~~~
    float: Percentage score (0-100)

serializable_value
    Return the value of the field name for this instance. If the field is
a foreign key, return the id value instead of the object. If there's
no Field object with this name on the model, return the model
attribute's value.

Used to serialize a field's value (in the serializer, or form output,
for example). Normally, you would just access the attribute directly
and not use this method.

time_remaining
    Calculates the remaining time for the quiz in seconds.


Returns
~~~~~~~~
    int: Seconds remaining, or 0 if the time limit has been exceeded

unique_error_message
    No documentation available.

validate_constraints
    No documentation available.

validate_unique
    Check unique constraints on the model and raise ValidationError if any
failed.

QuizResponse
------------

Represents a user's response to a single question within a quiz attempt.

Tracks which question was asked, which choice was selected, and whether
the answer was correct.

Fields
~~~~~~


id
    Type: BigAutoField
    Description: 

quiz_attempt
    Type: ForeignKey
    Description: The quiz attempt this response belongs to

question
    Type: ForeignKey
    Description: The question that was answered

selected_choice
    Type: ForeignKey
    Description: The choice that was selected

is_correct
    Type: BooleanField
    Description: Whether this response was correct

response_time
    Type: DateTimeField
    Description: When this question was answered

Methods
~~~~~~~

adelete
    No documentation available.

arefresh_from_db
    No documentation available.

asave
    No documentation available.

clean
    Hook for doing any extra model-wide validation after clean() has been
called on every field by self.clean_fields. Any ValidationError raised
by this method will not be associated with a particular field; it will
have a special-case association with the field defined by NON_FIELD_ERRORS.

clean_fields
    Clean all fields and raise a ValidationError containing a dict
of all validation errors if any occur.

date_error_message
    No documentation available.

delete
    No documentation available.

full_clean
    Call clean_fields(), clean(), validate_unique(), and
validate_constraints() on the model. Raise a ValidationError for any
errors that occur.

get_constraints
    No documentation available.

get_deferred_fields
    Return a set containing names of deferred fields for this instance.

get_next_by_response_time
    No documentation available.

get_previous_by_response_time
    No documentation available.

prepare_database_save
    No documentation available.

refresh_from_db
    Reload field values from the database.

By default, the reloading happens from the database this instance was
loaded from, or by the read router if this instance wasn't loaded from
any database. The using parameter will override the default.

Fields can be used to specify which fields to reload. The fields
should be an iterable of field attnames. If fields is None, then
all non-deferred fields are reloaded.

When accessing deferred fields of an instance, the deferred loading
of the field will call this method.

save
    Override save method to automatically set is_correct based on the selected choice.

save_base
    Handle the parts of saving which should be done only once per save,
yet need to be done in raw saves, too. This includes some sanity
checks and signal sending.

The 'raw' argument is telling save_base not to save any parent
models and not to do any changes to the values before save. This
is used by fixture loading.

serializable_value
    Return the value of the field name for this instance. If the field is
a foreign key, return the id value instead of the object. If there's
no Field object with this name on the model, return the model
attribute's value.

Used to serialize a field's value (in the serializer, or form output,
for example). Normally, you would just access the attribute directly
and not use this method.

unique_error_message
    No documentation available.

validate_constraints
    No documentation available.

validate_unique
    Check unique constraints on the model and raise ValidationError if any
failed.

UserProfile
-----------

Extends the built-in User model with additional profile information.

This model is connected to the User model with a one-to-one relationship
and is automatically created/updated when the User model is saved.

Fields
~~~~~~


id
    Type: BigAutoField
    Description: 

user
    Type: OneToOneField
    Description: The user this profile belongs to

bio
    Type: TextField
    Description: Short biography or description

avatar
    Type: FileField
    Description: Profile picture

favorite_category
    Type: ForeignKey
    Description: User's favorite quiz category

date_of_birth
    Type: DateField
    Description: User's date of birth

created_at
    Type: DateTimeField
    Description: When the profile was created

updated_at
    Type: DateTimeField
    Description: When the profile was last updated

Methods
~~~~~~~

adelete
    No documentation available.

arefresh_from_db
    No documentation available.

asave
    No documentation available.

average_score
    Return the user's average score across all quizzes.

clean
    Hook for doing any extra model-wide validation after clean() has been
called on every field by self.clean_fields. Any ValidationError raised
by this method will not be associated with a particular field; it will
have a special-case association with the field defined by NON_FIELD_ERRORS.

clean_fields
    Clean all fields and raise a ValidationError containing a dict
of all validation errors if any occur.

date_error_message
    No documentation available.

delete
    No documentation available.

full_clean
    Call clean_fields(), clean(), validate_unique(), and
validate_constraints() on the model. Raise a ValidationError for any
errors that occur.

get_constraints
    No documentation available.

get_deferred_fields
    Return a set containing names of deferred fields for this instance.

get_next_by_created_at
    No documentation available.

get_next_by_updated_at
    No documentation available.

get_previous_by_created_at
    No documentation available.

get_previous_by_updated_at
    No documentation available.

prepare_database_save
    No documentation available.

refresh_from_db
    Reload field values from the database.

By default, the reloading happens from the database this instance was
loaded from, or by the read router if this instance wasn't loaded from
any database. The using parameter will override the default.

Fields can be used to specify which fields to reload. The fields
should be an iterable of field attnames. If fields is None, then
all non-deferred fields are reloaded.

When accessing deferred fields of an instance, the deferred loading
of the field will call this method.

save
    Save the current instance. Override this in a subclass if you want to
control the saving process.

The 'force_insert' and 'force_update' parameters can be used to insist
that the "save" must be an SQL insert or update (or equivalent for
non-SQL backends), respectively. Normally, they should not be set.

save_base
    Handle the parts of saving which should be done only once per save,
yet need to be done in raw saves, too. This includes some sanity
checks and signal sending.

The 'raw' argument is telling save_base not to save any parent
models and not to do any changes to the values before save. This
is used by fixture loading.

serializable_value
    Return the value of the field name for this instance. If the field is
a foreign key, return the id value instead of the object. If there's
no Field object with this name on the model, return the model
attribute's value.

Used to serialize a field's value (in the serializer, or form output,
for example). Normally, you would just access the attribute directly
and not use this method.

total_quizzes_taken
    Return the total number of quizzes completed by the user.

unique_error_message
    No documentation available.

validate_constraints
    No documentation available.

validate_unique
    Check unique constraints on the model and raise ValidationError if any
failed.
