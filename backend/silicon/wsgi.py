"""
WSGI config for silicon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
import environ
from pathlib import Path


env = environ.Env(DEBUG=(bool, False))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

environment = env('ENVIRONMENT')

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'silicon.settings.' + environment)

application = get_wsgi_application()
