Installation Guide
=================

This guide provides step-by-step instructions for setting up the Quiz Game application
in your local environment.

Prerequisites
------------

Before installing the Quiz Game application, ensure you have the following installed:

* Python 3.8 or higher
* pip (Python package manager)
* Git (for cloning the repository)
* Virtual environment (recommended)

System Requirements
------------------

* **Operating System**: Windows, macOS, or Linux
* **RAM**: 2GB minimum, 4GB recommended
* **Disk Space**: 100MB for application and dependencies

Step-by-Step Installation
-------------------------

1. Clone the Repository
~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   git clone https://github.com/yourusername/quiz-game.git
   cd quiz-game

2. Create and Activate Virtual Environment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Windows:

.. code-block:: bash

   python -m venv venv
   venv\Scripts\activate

macOS/Linux:

.. code-block:: bash

   python -m venv venv
   source venv/bin/activate

3. Install Dependencies
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash

   pip install -r requirements.txt

4. Database Setup
~~~~~~~~~~~~~~~

Run migrations to create the database schema:

.. code-block:: bash

   python manage.py migrate

5. Create Superuser (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Create an admin user to manage the application:

.. code-block:: bash

   python manage.py createsuperuser

Follow the prompts to set username, email, and password.

6. Load Sample Data (Optional)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Load sample quizzes and questions:

.. code-block:: bash

   python manage.py loaddata sample_quizzes

7. Run Development Server
~~~~~~~~~~~~~~~~~~~~~~~

Start the Django development server:

.. code-block:: bash

   python manage.py runserver

8. Access the Application
~~~~~~~~~~~~~~~~~~~~~~~

Open your web browser and navigate to:

* Main application: http://127.0.0.1:8000/
* Admin interface: http://127.0.0.1:8000/admin/

Configuration Options
--------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~

The following environment variables can be set to customize the application:

* ``DEBUG``: Set to ``False`` in production (default: ``True``)
* ``SECRET_KEY``: Django secret key for cryptographic signing
* ``DATABASE_URL``: Database connection string (default: SQLite)

Custom Settings
~~~~~~~~~~~~~

To override default settings, create a ``local_settings.py`` file in the ``quiz_project`` directory.

Example:

.. code-block:: python

   # quiz_project/local_settings.py
   DEBUG = False
   ALLOWED_HOSTS = ['quizgame.example.com']
   
   # Database configuration
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'NAME': 'quiz_db',
           'USER': 'quiz_user',
           'PASSWORD': 'secure_password',
           'HOST': 'localhost',
           'PORT': '5432',
       }
   }

Troubleshooting
--------------

Common Issues
~~~~~~~~~~~

1. **Migration Errors**

   If you encounter migration errors:

   .. code-block:: bash

      python manage.py migrate --fake-initial

2. **Static Files Not Loading**

   Collect static files:

   .. code-block:: bash

      python manage.py collectstatic

3. **Package Dependencies**

   If you encounter missing dependencies:

   .. code-block:: bash

      pip install -r requirements.txt --upgrade

Getting Help
~~~~~~~~~~

If you encounter any issues during installation:

* Check the project's GitHub issues
* Consult the Django documentation
* Reach out to the maintainers 