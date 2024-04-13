from .base import *



EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# # Database
# # https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}