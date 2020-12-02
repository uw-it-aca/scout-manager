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

MANAGER_SUPERUSER_GROUP = "u_acadev_tester"
