# Copyright 2025 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name="scout_manager",
    version="0.1",
    packages=["scout_manager"],
    include_package_data=True,
    install_requires=[
        "beautifulsoup4",
        "django~=2.2",
        "django-compressor==2.4.1",
        "django-pyscss",
        "django-user-agents",
        "Django-SupportTools",
        'Django-UserService',
        "html5lib",
        "openpyxl<=2.6.4",
        "pillow",
        "pytz",
        "setuptools",
        "UW-Django-SAML2",
        "UW-RestClients-GWS~=2.3",
        "lxml==4.9.4",
        "xmlsec==1.3.13"
    ],
    license="Apache License, Version 2.0",  # example license
    description="A Django app for managing spaces in spotseeker_server.",
    long_description=README,
    url="https://github.com/uw-it-aca/scout-manager/",
    author="UW-IT AXDD",
    author_email="aca-it@uw.edu",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
