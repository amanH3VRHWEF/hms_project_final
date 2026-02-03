import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY: Pulled from .env (defaults to local-key if not found)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-default-key')

# SECURITY: Set to False in production
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third Party
    'rest_framework',

    # Your Apps
    'appointments',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hms_main.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'hms_main.wsgi.application'

# Database Connection
# Pulling password from .env for security
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'hms_db'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'aman@2007'), # Set this in .env
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}

# --- GOOGLE CALENDAR CONFIGURATION ---
# Points to the credentials file you downloaded from Google Console
GOOGLE_CREDENTIALS_FILE = os.path.join(BASE_DIR, 'appointments', 'credentials.json')
GOOGLE_TOKEN_FILE = os.path.join(BASE_DIR, 'appointments', 'token.json')

# --- SERVERLESS EMAIL CONFIGURATION ---
LAMBDA_URL = os.getenv('LAMBDA_URL', 'http://localhost:3000/dev/send-email')

# --- AUTHENTICATION ---
AUTH_USER_MODEL = 'appointments.User'

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Login/Logout Redirects
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'login'
LOGIN_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
