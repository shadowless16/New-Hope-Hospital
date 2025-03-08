import os
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import format_html

# Configure Django settings
settings.configure(
    TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(os.path.dirname(__file__), 'templates')],
    }],
    INSTALLED_APPS=[
        'django.contrib.contenttypes',
    ],
)

# Define the pages to render
pages = [
    {'template': 'index.html', 'output': 'dist/index.html'},
    # Add other pages as needed
]

# Render each page
for page in pages:
    rendered_html = render_to_string(page['template'])
    output_path = os.path.join(os.path.dirname(__file__), page['output'])
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(format_html(rendered_html))
