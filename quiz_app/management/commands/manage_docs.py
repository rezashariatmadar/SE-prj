from django.core.management.base import BaseCommand, CommandError
import os
import re
from datetime import datetime
from .doc_templates import TEMPLATES
from .doc_validator import DocValidator
from .doc_generator import DocGenerator

class Command(BaseCommand):
    help = 'Manages documentation files (create, update, delete, generate, validate)'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Action to perform (create, update, delete, generate, validate)')
        parser.add_argument('--title', type=str, help='Title of the documentation section')
        parser.add_argument('--content', type=str, help='Content of the documentation')
        parser.add_argument('--file', type=str, help='Name of the documentation file (without .rst extension)')
        parser.add_argument('--section', type=str, help='Section to add content to (for update action)')
        parser.add_argument('--template', type=str, help='Template to use (api, model, view, form)')
        parser.add_argument('--app', type=str, help='App name for generating documentation')
        parser.add_argument('--validate', action='store_true', help='Validate documentation after changes')

    def handle(self, *args, **options):
        action = options['action']
        docs_dir = 'docs'

        if action == 'create':
            self.create_doc(options)
        elif action == 'update':
            self.update_doc(options)
        elif action == 'delete':
            self.delete_doc(options)
        elif action == 'generate':
            self.generate_docs(options)
        elif action == 'validate':
            self.validate_docs()
        else:
            raise CommandError(f'Unknown action: {action}')

    def create_doc(self, options):
        """Create a new documentation file."""
        if not options['file'] or not options['title']:
            raise CommandError('--file and --title are required for create action')

        file_name = f"{options['file']}.rst"
        file_path = os.path.join('docs', file_name)

        if os.path.exists(file_path):
            raise CommandError(f'File {file_name} already exists')

        # Use template if specified
        if options.get('template'):
            if options['template'] not in TEMPLATES:
                raise CommandError(f'Unknown template: {options["template"]}')
            
            template = TEMPLATES[options['template']]
            content = template.format(
                title=options['title'],
                date=datetime.now().strftime('%Y-%m-%d'),
                overview=options.get('content', ''),
                endpoints='',
                authentication='',
                error_handling='',
                examples='',
                fields='',
                methods='',
                relationships='',
                url_pattern='',
                context_data='',
                template='',
                validation=''
            )
        else:
            # Create basic content
            content = f"""{options['title']}
{'=' * len(options['title'])}

Last updated: {datetime.now().strftime('%Y-%m-%d')}

{options.get('content', '')}
"""

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Update index.rst to include the new file
        self.update_index(file_name)
        
        # Validate if requested
        if options.get('validate'):
            self.validate_file(file_path)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully created {file_name}'))

    def update_doc(self, options):
        """Update an existing documentation file."""
        if not options['file']:
            raise CommandError('--file is required for update action')

        file_name = f"{options['file']}.rst"
        file_path = os.path.join('docs', file_name)

        if not os.path.exists(file_path):
            raise CommandError(f'File {file_name} does not exist')

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Update last modified date
        content = re.sub(
            r'Last updated: \d{4}-\d{2}-\d{2}',
            f'Last updated: {datetime.now().strftime("%Y-%m-%d")}',
            content
        )

        # Add new content if provided
        if options.get('content'):
            if options.get('section'):
                # Find the section and add content after it
                section_pattern = f"{options['section']}\n[-=~]+\n"
                if re.search(section_pattern, content):
                    content = re.sub(
                        section_pattern,
                        f"{options['section']}\n{'=' * len(options['section'])}\n\n{options['content']}\n\n",
                        content
                    )
                else:
                    content += f"\n\n{options['section']}\n{'=' * len(options['section'])}\n\n{options['content']}\n"
            else:
                content += f"\n\n{options['content']}\n"

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        # Validate if requested
        if options.get('validate'):
            self.validate_file(file_path)
            
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {file_name}'))

    def delete_doc(self, options):
        """Delete a documentation file."""
        if not options['file']:
            raise CommandError('--file is required for delete action')

        file_name = f"{options['file']}.rst"
        file_path = os.path.join('docs', file_name)

        if not os.path.exists(file_path):
            raise CommandError(f'File {file_name} does not exist')

        os.remove(file_path)
        self.update_index(file_name, remove=True)
        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {file_name}'))

    def generate_docs(self, options):
        """Generate documentation from docstrings."""
        if not options.get('app'):
            raise CommandError('--app is required for generate action')

        generator = DocGenerator()
        docs = generator.generate_all_docs(options['app'])

        # Create or update documentation files
        for doc_type, content in docs.items():
            file_name = f"{options['app']}_{doc_type}.rst"
            file_path = os.path.join('docs', file_name)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            self.update_index(file_name)
            
            if options.get('validate'):
                self.validate_file(file_path)
            
            self.stdout.write(self.style.SUCCESS(f'Generated {file_name}'))

    def validate_docs(self):
        """Validate all documentation files."""
        validator = DocValidator()
        docs_dir = 'docs'
        
        for root, dirs, files in os.walk(docs_dir):
            for file in files:
                if file.endswith('.rst'):
                    file_path = os.path.join(root, file)
                    self.validate_file(file_path)

    def validate_file(self, file_path):
        """Validate a single documentation file."""
        validator = DocValidator()
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = validator.validate_rst_file(content)
        
        if issues:
            self.stdout.write(self.style.WARNING(f'\nIssues found in {file_path}:'))
            for issue in issues:
                self.stdout.write(self.style.WARNING(
                    f'Line {issue["line"]}: {issue["message"]} ({issue["type"]})'
                ))
        else:
            self.stdout.write(self.style.SUCCESS(f'No issues found in {file_path}'))

    def update_index(self, file_name, remove=False):
        """Update index.rst to include or remove a file."""
        index_path = os.path.join('docs', 'index.rst')
        if not os.path.exists(index_path):
            return

        with open(index_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Find the toctree directive
        toctree_pattern = r'\.\. toctree::\n\s+:maxdepth: \d+\n\s+:caption: Contents:\n\n((?:\s+[^\n]+\n)*)'
        match = re.search(toctree_pattern, content)
        
        if match:
            toctree_content = match.group(1)
            if remove:
                # Remove the file from toctree
                new_toctree = re.sub(f'\s+{file_name[:-4]}\n', '', toctree_content)
            else:
                # Add the file to toctree if not already present
                if file_name[:-4] not in toctree_content:
                    new_toctree = toctree_content + f'   {file_name[:-4]}\n'
                else:
                    new_toctree = toctree_content

            # Update the content
            new_content = re.sub(
                toctree_pattern,
                f'.. toctree::\n   :maxdepth: 2\n   :caption: Contents:\n\n{new_toctree}',
                content
            )

            with open(index_path, 'w', encoding='utf-8') as f:
                f.write(new_content) 