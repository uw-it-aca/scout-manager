# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .base_settings import *
# BASE_DIR = os.path.dirname(os.path.dirname(__file__))

if os.getenv('ENV', 'localdev') == 'localdev':
    DEBUG = True
else:
    DEBUG = False

INSTALLED_APPS += [
    # 'django_sass',
    'scout_manager',
    # 'scout',
    # 'restclients',
    # 'spotseeker_restclient',
    'django_user_agents',
    'compressor',
    'userservice',
    'supporttools'
]

MIDDLEWARE += [
    'django.middleware.security.SecurityMiddleware',
    # 'django.contrib.auth.middleware.RemoteUserMiddleware',
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
MANAGER_SUPERUSER_GROUP = os.getenv('MANAGER_SUPERUSER_GROUP', 'u_acadev_tester')
USERSERVICE_ADMIN_GROUP = os.getenv('USERSERVICE_ADMIN_GROUP', '')
AUTHZ_GROUP_BACKEND = os.getenv('AUTHZ_GROUP_BACKEND', '')

# spotseeker server api stuff
RESTCLIENTS_SPOTSEEKER_HOST = os.getenv('RESTCLIENTS_SPOTSEEKER_HOST', None)
RESTCLIENTS_SPOTSEEKER_DAO_CLASS = os.getenv('RESTCLIENTS_SPOTSEEKER_DAO_CLASS', 'Mock')
SPOTSEEKER_OAUTH_KEY = os.getenv('SPOTSEEKER_OAUTH_KEY', '')
SPOTSEEKER_OAUTH_SECRET = os.getenv('SPOTSEEKER_OAUTH_SECRET', '')
OAUTH_USER = os.getenv('OAUTH_USER', '')
