# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from google.oauth2 import service_account
from .base_settings import *

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

# django storages settings
if not DEBUG:
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.getenv('STORAGE_BUCKET_NAME', '')
    GS_PROJECT_ID = os.getenv('STORAGE_PROJECT_ID')
    GS_LOCATION = os.path.join(os.getenv('ENV'), 'manager')
    GS_CREDENTIALS = service_account.Credentials.from_service_account_file(
        '/gcs/credentials.json'
    )

# scout auth stuff
MANAGER_SUPERUSER_GROUP = os.getenv('MANAGER_SUPERUSER_GROUP', 'u_acadev_test')
USERSERVICE_ADMIN_GROUP = os.getenv('USERSERVICE_ADMIN_GROUP', 'u_acadev_test')

# spotseeker server api stuff
RESTCLIENTS_SPOTSEEKER_HOST = os.getenv('RESTCLIENTS_SPOTSEEKER_HOST', None)
RESTCLIENTS_SPOTSEEKER_DAO_CLASS = os.getenv('RESTCLIENTS_SPOTSEEKER_DAO_CLASS', 'Mock')
SPOTSEEKER_OAUTH_KEY = os.getenv('SPOTSEEKER_OAUTH_KEY', '')
SPOTSEEKER_OAUTH_SECRET = os.getenv('SPOTSEEKER_OAUTH_SECRET', '')
OAUTH_USER = os.getenv('OAUTH_USER', '')
