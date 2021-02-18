import os
from setuptools import setup

README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='scout_manager',
    version='0.1',
    packages=['scout_manager'],
    include_package_data=True,
    install_requires = [
        'beautifulsoup4',
        'django>=1.10,<1.11',
        'django-compressor',
        'django-pyscss',
        'django-user-agents',
        'django-storages[google]',
        'Django-SupportTools>1.3,<2.0',
        'Django-UserService==1.4.0',
        'html5lib<=0.9999999',
        'openpyxl<=2.6.4',
        'pillow',
        'pytz',
        'setuptools',
        'UW-RestClients-GWS==1.0',  
    ],
    license='Apache License, Version 2.0',  # example license
    description='A Django app for developer resources complimentary to mdot_web client.',
    long_description=README,
    url='http://www.example.com/',
    author='Your Name',
    author_email='yourname@example.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
