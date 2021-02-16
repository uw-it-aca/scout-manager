# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .base_settings import *
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if os.getenv('ENV', 'localdev') == 'localdev':
    DEBUG = True
else:
    DEBUG = False

INSTALLED_APPS += [
    'scout_manager',
    'django_user_agents',
    'compressor',
    'userservice',
    'supporttools'
]

MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'userservice.user.UserServiceMiddleware',
]

STATICFILES_FINDERS += (
    'compressor.finders.CompressorFinder',
)


COMPRESS_PRECOMPILERS = (
    ("text/x-scss", "django_pyscss.compressor.DjangoScssFilter",),
    ("text/x-sass", "django_pyscss.compressor.DjangoScssFilter",),
    ('text/less', 'lessc {infile} {outfile}'),
)

# scout auth stuff
MANAGER_SUPERUSER_GROUP = os.getenv('MANAGER_SUPERUSER_GROUP', 'u_acadev_test')
USERSERVICE_ADMIN_GROUP = os.getenv('USERSERVICE_ADMIN_GROUP', 'u_acadev_test')
AUTHZ_GROUP_BACKEND = os.getenv('AUTHZ_GROUP_BACKEND', '')

# spotseeker server api stuff
RESTCLIENTS_SPOTSEEKER_HOST = os.getenv('RESTCLIENTS_SPOTSEEKER_HOST', None)
RESTCLIENTS_SPOTSEEKER_DAO_CLASS = os.getenv('RESTCLIENTS_SPOTSEEKER_DAO_CLASS', 'Mock')
SPOTSEEKER_OAUTH_KEY = os.getenv('SPOTSEEKER_OAUTH_KEY', '')
SPOTSEEKER_OAUTH_SECRET = os.getenv('SPOTSEEKER_OAUTH_SECRET', '')
OAUTH_USER = os.getenv('OAUTH_USER', '')
