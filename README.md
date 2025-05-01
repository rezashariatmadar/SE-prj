# Django Quiz Application

A web-based quiz application built with Django that allows users to take quizzes across various categories.

## Features

- **Multiple quiz categories**: Create and organize questions by topics
- **User authentication**: Register, login, and track progress
- **Score tracking**: Save and display quiz results and statistics
- **Admin interface**: Comprehensive management for quizzes and users
- **Automated question generation**: Tools for creating content
- **Responsive design**: Mobile-friendly interface with Bootstrap 4
- **Documentation automation**: Built-in tools for generating documentation

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd <repository-name>
```

2. **Create and activate virtual environment**
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Apply migrations**
```bash
python manage.py migrate
```

5. **Create superuser** (optional)
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

## Usage

1. **Access the application** at `http://localhost:8000`
2. **Register a new account** or login with existing credentials
3. **Browse available quiz categories** from the homepage
4. **Select a quiz** and customize number of questions and time limit
5. **Answer questions** within the allocated time
6. **View your results** and track progress in your profile

## Admin Interface

Access the admin interface at `http://localhost:8000/admin` to:
- **Manage quiz categories**: Create, edit, and delete categories
- **Add/edit questions**: Create questions with multiple choice answers
- **View user results**: Monitor quiz attempts and scores
- **Manage user accounts**: Add, edit, or deactivate users

## Populating Questions

Use the management command to populate the database with sample questions:
```bash
python manage.py populate_questions --questions_per_category 10 --choices_per_question 4
```

## Documentation

This project includes a comprehensive documentation system with automation tools:

### Building Documentation

Generate documentation in various formats:
```bash
# Generate Word document
python docs/docs_workflow.py --output-format word

# Generate all formats (HTML, Word, LaTeX, PDF)
python docs/docs_workflow.py
```

### Documentation Management

Create and manage documentation files:
```bash
# Create a new documentation file
python manage.py manage_docs create --file new_doc --title "New Document"

# Generate documentation from docstrings
python manage.py manage_docs generate --app quiz_app

# Validate documentation
python manage.py manage_docs validate
```

For more details, see the [Documentation Tools](docs/documentation_tools.rst) and [Documentation Workflow](docs/documentation_workflow.rst) guides.

## Technology Stack

- **Backend**: Django web framework
- **Database**: SQLite (production deployments can use PostgreSQL)
- **Frontend**: Bootstrap 4, HTML5, CSS3, JavaScript
- **Forms**: django-crispy-forms for improved form rendering
- **Development tools**: django-debug-toolbar, django-extensions
- **Documentation**: Sphinx, docxbuilder
- **Data visualization**: pandas, matplotlib, seaborn

## Project Structure

- **quiz_project/**: Main Django project settings
- **quiz_app/**: Core application code
  - **models.py**: Database models
  - **views.py**: View controllers
  - **forms.py**: Form definitions
  - **admin.py**: Admin interface customization
  - **templates/**: HTML templates
  - **tests/**: Automated tests
- **scripts/**: Utility scripts
- **docs/**: Documentation files
- **templates/**: Project-wide templates

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 