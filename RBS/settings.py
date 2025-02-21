"""
Django settings for RBS project.

Generated by 'django-admin startproject' using Django 4.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e*-@hm*td&7nev*+r39w-%4^!v@2crth$czi43i%glqhcj)bm4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['www.rbscotlandinternational.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'transactions',
    'loans',
    'investments',
    'users',
    'core',
    'admin_dashboard',
    'btc',
    'cards',


    'widget_tweaks'
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

ROOT_URLCONF = 'RBS.urls'

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

WSGI_APPLICATION = 'RBS.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# default static files settings for PythonAnywhere.
# see https://help.pythonanywhere.com/pages/DjangoStaticFiles for more info
MEDIA_ROOT = '/home/theabcgame/RBS/media'
MEDIA_URL = '/media/'
STATIC_ROOT = '/home/theabcgame/RBS/static'
STATIC_URL = '/static/'



LOGIN_URL = 'authenticating:login'

LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

AUTHENTICATION_BACKENDS = ['users.backends.EmailBackend']

# Email Configuration
'''EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.zoho.com'
EMAIL_PORT = 465  # You can also use 587 if you prefer TLS
EMAIL_USE_SSL = True  # Change to EMAIL_USE_TLS = True if using port 587
EMAIL_HOST_USER = 'support@nonresidentsuk.com'
EMAIL_HOST_PASSWORD = 'Pass@2024'
DEFAULT_FROM_EMAIL = 'RBS Non Resident <support@nonresidentsuk.com>'


SESSION_COOKIE_AGE = 120  # 2 minutes in seconds
SESSION_SAVE_EVERY_REQUEST = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
'''


import json
import os

# Load email configuration
email_config_path = os.path.join(BASE_DIR, 'email_config.json')
with open(email_config_path, 'r') as f:
    email_config = json.load(f)

# Set email settings
EMAIL_BACKEND = email_config['EMAIL_BACKEND']
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_PORT = email_config['EMAIL_PORT']
EMAIL_USE_SSL = email_config['EMAIL_USE_SSL']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL = email_config['DEFAULT_FROM_EMAIL']

# Load session configuration
session_config_path = os.path.join(BASE_DIR, 'session_config.json')
with open(session_config_path, 'r') as f:
    session_config = json.load(f)

# Set session settings
SESSION_COOKIE_AGE = session_config['SESSION_COOKIE_AGE']
SESSION_SAVE_EVERY_REQUEST = session_config['SESSION_SAVE_EVERY_REQUEST']
SESSION_EXPIRE_AT_BROWSER_CLOSE = session_config['SESSION_EXPIRE_AT_BROWSER_CLOSE']






