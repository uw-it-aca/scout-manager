# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from .base_settings import *

if os.getenv("ENV", "localdev") == "localdev":
    DEBUG = True
else:
    DEBUG = False

INSTALLED_APPS += [
    "scout_manager",
    "django_user_agents",
    "compressor",
    "userservice",
    "supporttools",
]

APP_NAME = os.getenv("APP_NAME", "scout-manager")

MIDDLEWARE += [
    "django.middleware.security.SecurityMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "userservice.user.UserServiceMiddleware",
]

STATICFILES_FINDERS += ("compressor.finders.CompressorFinder",)


COMPRESS_PRECOMPILERS = (
    (
        "text/x-scss",
        "django_pyscss.compressor.DjangoScssFilter",
    ),
    (
        "text/x-sass",
        "django_pyscss.compressor.DjangoScssFilter",
    ),
    ("text/less", "lessc {infile} {outfile}"),
)

TEMPLATES[0]["OPTIONS"]["context_processors"].extend(
    [
        "scout.context_processors.google_maps",
        "scout.context_processors.google_analytics",
        "scout.context_processors.is_desktop",
    ]
)

GOOGLE_MAPS_API = os.getenv("GOOGLE_MAPS_API", "")

# scout auth stuff
SCOUT_MANAGER_ACCESS_GROUP = os.getenv(
    "SCOUT_MANAGER_ACCESS_GROUP", "u_acadev_scout_access_test"
)
MANAGER_SUPERUSER_GROUP = os.getenv(
    "MANAGER_SUPERUSER_GROUP", "u_acadev_tester"
)
USERSERVICE_ADMIN_GROUP = os.getenv(
    "USERSERVICE_ADMIN_GROUP", "u_acadev_tester"
)

# spotseeker server api stuff
RESTCLIENTS_SPOTSEEKER_HOST = os.getenv("RESTCLIENTS_SPOTSEEKER_HOST", None)
RESTCLIENTS_SPOTSEEKER_DAO_CLASS = os.getenv(
    "RESTCLIENTS_SPOTSEEKER_DAO_CLASS", "Mock"
)

SPOTSEEKER_OAUTH_CREDENTIAL = os.getenv("SPOTSEEKER_OAUTH_CREDENTIAL", "")
SPOTSEEKER_OAUTH_SCOPE = os.getenv("SPOTSEEKER_OAUTH_SCOPE", "read write")
OAUTH_USER = os.getenv("OAUTH_USER", "")

SPOTSEEKER_TECHLOAN_UPDATER = {
    "server_host": RESTCLIENTS_SPOTSEEKER_HOST,
    "oauth_credential": SPOTSEEKER_OAUTH_CREDENTIAL,
    "oauth_scope": SPOTSEEKER_OAUTH_SCOPE,
    "oauth_user": OAUTH_USER,
}

SPOTSEEKER_TECHLOAN_URL = os.getenv("SPOTSEEKER_TECHLOAN_URL", None)

if os.getenv("AUTH", "NONE") == "SAML_MOCK":
    MOCK_SAML_ATTRIBUTES["isMemberOf"].append(SCOUT_MANAGER_ACCESS_GROUP)

DEBUG_CACHING = os.getenv("DEBUG_CACHING", "True") == "True"

if DEBUG and not DEBUG_CACHING:
    CACHES = {
        "default": {
            "BACKEND": "django.core.cache.backends.dummy.DummyCache",
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'scout-manager',
        }
    }
