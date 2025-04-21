"""
WSGI config for production environment.
"""

import os

from django.core.wsgi import get_wsgi_application

# Explicitly set Django settings module for production
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.production_settings')

application = get_wsgi_application() 