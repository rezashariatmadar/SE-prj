"""Documentation validation utilities."""

import re
from typing import List, Dict, Any

class DocValidator:
    """Validates RST documentation files for common issues."""

    @staticmethod
    def validate_rst_file(content: str) -> List[Dict[str, Any]]:
        """Validate RST file content and return list of issues."""
        issues = []
        
        # Check title formatting
        title_pattern = r'^[^\n]+\n=+\n'
        if not re.match(title_pattern, content, re.MULTILINE):
            issues.append({
                'type': 'format',
                'message': 'Missing or incorrectly formatted title',
                'line': 1
            })

        # Check section formatting
        section_pattern = r'^[^\n]+\n-+\n'
        sections = re.finditer(section_pattern, content, re.MULTILINE)
        for section in sections:
            title = section.group().split('\n')[0]
            underline = section.group().split('\n')[1]
            if len(underline) < len(title):
                issues.append({
                    'type': 'format',
                    'message': f'Section underline too short: {title}',
                    'line': content[:section.start()].count('\n') + 1
                })

        # Check for broken links
        link_pattern = r':doc:`([^`]+)`'
        for match in re.finditer(link_pattern, content):
            link = match.group(1)
            if not any(link in line for line in content.split('\n')):
                issues.append({
                    'type': 'link',
                    'message': f'Broken documentation link: {link}',
                    'line': content[:match.start()].count('\n') + 1
                })

        # Check for code blocks
        code_block_pattern = r'::\n\n\s+[^\n]+\n'
        if not re.search(code_block_pattern, content):
            issues.append({
                'type': 'content',
                'message': 'No code examples found',
                'line': 0
            })

        # Check for images
        image_pattern = r'\.\. image:: ([^\n]+)'
        for match in re.finditer(image_pattern, content):
            image_path = match.group(1)
            if not image_path.startswith('_static/'):
                issues.append({
                    'type': 'image',
                    'message': f'Image path should be in _static directory: {image_path}',
                    'line': content[:match.start()].count('\n') + 1
                })

        return issues

    @staticmethod
    def validate_docstring(docstring: str) -> List[Dict[str, Any]]:
        """Validate Python docstring content."""
        issues = []
        
        if not docstring:
            issues.append({
                'type': 'docstring',
                'message': 'Missing docstring',
                'line': 0
            })
            return issues

        # Check for parameter documentation
        param_pattern = r':param\s+(\w+):'
        params = re.finditer(param_pattern, docstring)
        for param in params:
            param_name = param.group(1)
            if not re.search(rf':type\s+{param_name}:', docstring):
                issues.append({
                    'type': 'docstring',
                    'message': f'Missing type documentation for parameter: {param_name}',
                    'line': docstring[:param.start()].count('\n') + 1
                })

        # Check for return documentation
        if 'return' in docstring.lower() and not re.search(r':return:', docstring):
            issues.append({
                'type': 'docstring',
                'message': 'Missing return type documentation',
                'line': 0
            })

        return issues 