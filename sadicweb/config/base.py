"""
Base Django settings for Sadic project.
"""
import os
import sys
import glob
import sadicweb.core.sadicapp as sadicapp
from django.core.exceptions import ImproperlyConfigured
from django.core.management.utils import get_random_secret_key
from sadicweb.config.env import ENV, PROJECT_ROOT

#------------------------------------------------------------------------------
# Base Django config for SadicWeb
#------------------------------------------------------------------------------
VERSION = sadicapp.VERSION
BASE_DIR = PROJECT_ROOT()
ALLOWED_HOSTS = ENV.list('ALLOWED_HOSTS', default=['*'])
DEBUG = ENV.bool('DEBUG', default=False)
WSGI_APPLICATION = "sadicweb.config.wsgi.application"
ROOT_URLCONF = 'sadicweb.config.urls'

SECRET_KEY = ENV.str('SECRET_KEY', default='')
if len(SECRET_KEY) == 0:
    SECRET_KEY = get_random_secret_key()
    
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

STATIC_URL = '/static/'
STATIC_ROOT = ENV.str('STATIC_ROOT', default=PROJECT_ROOT('static_root'))
STATICFILES_DIRS = [
    PROJECT_ROOT('sadicweb/static'),
]

# Add local site static files if set
SITE_STATIC = ENV.str('SITE_STATIC', default='')
if len(SITE_STATIC) > 0:
    if os.path.isdir(SITE_STATIC):
        STATICFILES_DIRS.insert(0, SITE_STATIC)
    else:
        raise ImproperlyConfigured('SITE_STATIC should be a path to a directory')

# Add system site static files
if os.path.isdir('/usr/share/sadicweb/site/static'):
    STATICFILES_DIRS.insert(0, '/usr/share/sadicweb/site/static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'   

ROOT_URLCONF = "sadicweb.config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "sadicweb", "core", "sadicapp", "templates"),
        ],      
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]





# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"



#------------------------------------------------------------------------------
# Locale settings
#------------------------------------------------------------------------------
LANGUAGE_CODE = ENV.str('LANGUAGE_CODE', default='en-us')
TIME_ZONE = ENV.str('TIME_ZONE', default='UTC')
USE_I18N = True
USE_L10N = True
USE_TZ = True

#------------------------------------------------------------------------------
# Django Apps
#------------------------------------------------------------------------------

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

]

INSTALLED_APPS += [
    'crispy_forms',
    'crispy_bootstrap4',
    'channels',
]

INSTALLED_APPS += [
    'sadicweb.core.sadicapp',
]

# Configura Redis come backend per WebSocket
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer",
    },
}

ASGI_APPLICATION = "sadicweb.core.asgi.application"

#------------------------------------------------------------------------------
# Django Middleware
#------------------------------------------------------------------------------

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

#------------------------------------------------------------------------------
# Django authentication backend. See auth.py
#------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = []

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]



