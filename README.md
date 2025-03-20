# Django Quiz Application

A web-based quiz application built with Django that allows users to take quizzes across various categories.

## Features

- Multiple quiz categories
- User authentication and registration
- Score tracking and results
- Admin interface for quiz management
- Automated question generation
- Responsive design with Bootstrap 4
- Comprehensive documentation automation

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

2. Create and activate virtual environment
```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Apply migrations
```bash
python manage.py migrate
```

5. Create superuser (optional)
```bash
python manage.py createsuperuser
```

6. Run development server
```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://localhost:8000`
2. Register a new account or login
3. Browse available quiz categories
4. Select a quiz and answer questions
5. View your results and track progress

## Admin Interface

Access the admin interface at `http://localhost:8000/admin` to:
- Manage quiz categories
- Add/edit questions
- View user results
- Manage user accounts

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

- Django
- SQLite
- Bootstrap 4
- django-crispy-forms
- JavaScript
- Sphinx (documentation generation)
- pandas & matplotlib (data analysis)

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 