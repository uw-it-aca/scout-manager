"""
Django settings for travis builds.

Only things needed for travis tests that are not in the base.py go here.
"""
from __future__ import absolute_import
from .base import *


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'dummy key for travis'
