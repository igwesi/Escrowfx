import os
import environ
from pathlib import Path
from datetime import timedelta

env = environ.Env(DEBUG=(bool, False))
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = ['*']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'djoser',
    'corsheaders',
    'rest_framework',
    'graphene_django',
    'phonenumber_field',   
    'django_cryptography',    
    'rest_framework.authtoken',
    
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
    'health_check.contrib.migrations',
]

PROJECT_APPS = [
    'apps.accounts',
    'apps.Finance',
    'apps.chat',
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',    
    
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'silicon.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'silicon.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Lagos'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL  = 'static/'
MEDIA_URL   = 'media/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'plugins/static')
]
STATIC_ROOT = BASE_DIR / "plugins/assets"
MEDIA_ROOT  = BASE_DIR / "plugins/media_cdn"

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL     = "accounts.User"
CRYPTOGRAPHY_SALT   = SECRET_KEY

#
CORS_ALLOWED_ORIGINS = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "https://escrowfx.netlify.app",
]

# CORS_ALLOW_ALL_ORIGINS: True

CORS_ALLOW_METHODS = (
    "GET",
    "POST",
    "PUT",
    "PATCH",
    "DELETE",
    "OPTIONS",
)

CORS_ALLOW_HEADERS = (
    "accept",
    "Authorization",
    "content-Type",
    # "user-agent",
    # "x-csrftoken",
    # "x-requested-with",
)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

SIMPLE_JWT = {
    "JTI_CLAIM"                 : "jti",    
    "UPDATE_LAST_LOGIN"         : True,
    "BLACKLIST_AFTER_ROTATION"  : False,
    "ROTATE_REFRESH_TOKENS"     : False,
    "ALGORITHM"                 : "HS256",
    'USER_ID_FIELD'             : 'user_id',
    "SIGNING_KEY"               : SECRET_KEY,
    "AUTH_HEADER_TYPES"         : ("Bearer",),
    "AUTH_HEADER_NAME"          : "HTTP_AUTHORIZATION",

    "REFRESH_TOKEN_LIFETIME"    : timedelta(days=1),
    "ACCESS_TOKEN_LIFETIME"     : timedelta(minutes=30),
    "TOKEN_TYPE_CLAIM"          : "token_type",
    "TOKEN_USER_CLASS"          : "rest_framework_simplejwt.models.TokenUser",
    "AUTH_TOKEN_CLASSES"        : ("rest_framework_simplejwt.tokens.AccessToken",),
    "USER_AUTHENTICATION_RULE"  : "rest_framework_simplejwt.authentication.default_user_authentication_rule",
}

DJOSER = {    
    "SET_USERNAME_RETYPE"                   : True,
    "SET_PASSWORD_RETYPE"                   : True,
    "SEND_ACTIVATION_EMAIL"                 : True,
    "SEND_CONFIRMATION_EMAIL"               : True,
    "USER_CREATE_PASSWORD_RETYPE"           : True,
    "USERNAME_CHANGED_EMAIL_CONFIRMATION"   : True,
    "PASSWORD_CHANGED_EMAIL_CONFIRMATION"   : True,    
    "LOGIN_FIELD"                           : "email",
    "USER_ID_FIELD"                         : "user_id,",
    "ACTIVATION_URL"                        : "activate/{uid}/{token}",
    "PASSWORD_RESET_CONFIRM_URL"            : "password/reset/confirm/{uid}/{token}",
    "USERNAME_RESET_CONFIRM_URL"            : "email/reset/confirm/{uid}/{token}",
    
    "SERIALIZERS": {
        'user_create'   : 'apps.accounts.api.serializers.UserRegistrationSerializer',
        'user'          : 'apps.accounts.api.serializers.UserProfileSerializer',
        'user_delete'   : 'djoser.serializers.UserDeleteSerializer',
    },
}

GRAPH_API_URL    = env('GRAPH_API_URL')
GRAPH_ACCESS_KEY = env('GRAPH_ACCESS_KEY')
GRAPH_WEBHOOK_DOMAIN = env('GRAPH_WEBHOOK_DOMAIN')