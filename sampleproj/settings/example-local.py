"""
Django settings for local builds.

This file is an example, copy it to local.py to override settings for your own
build.
"""
from __future__ import absolute_import
from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'set this to something random, please'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['*']

INSTALLED_APPS += (
#    'django.contrib.admin',
#    'django.contrib.messages',
    'scout',
    'compressor',
    'userservice',
    'supporttools'
)

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
#                'django.contrib.messages.context_processors.messages',
                'scout.context_processors.google_analytics',
                'scout.context_processors.is_desktop',
                'scout.context_processors.is_hybrid',
            ],
        },
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
STATIC_URL = '/static/'
STATIC_ROOT = '/tmp/'
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "compressor.finders.CompressorFinder",
)

# django-mobileesp
from django_mobileesp.detector import mobileesp_agent as agent
DETECT_USER_AGENTS = {
    'is_tablet' : agent.detectTierTablet,
    'is_mobile': agent.detectMobileQuick,
    'is_and': agent.detectAndroid,
    'is_ios': agent.detectIos,
    'is_win': agent.detectWindowsPhone,
}

# django-compressor
COMPRESS_PRECOMPILERS = (
    ('text/x-sass', 'django_pyscss.compressor.DjangoScssFilter'),
    ('text/x-scss', 'django_pyscss.compressor.DjangoScssFilter'),
)

# google analytics tracking
#GOOGLE_ANALYTICS_KEY = "UA-XXXXXXXX-X"

# django-userservice settings
#USERSERVICE_ADMIN_GROUP = ''
#AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation.all_ok.AllOK'

# oauth username for POSTing to spotseeker_server
#OAUTH_USER = ''
