SCOUT MANAGER
=============

This README documents whatever steps are necessary to get your application up and running.

## Installing the application ##

**Install Scout Manager app in your existing project**  

    $ (yourenv) pip install -e git+https://github.com/uw-it-aca/scout-manager/#egg=scout_manager

**Update your project urls.py**

    urlpatterns = patterns('',
        ...
        url(r'^manager/', include('scout_manager.urls')),
    )

**Update your project settings.py**

    INSTALLED_APPS = (
        ...
        'scout_manager',
        'scout',
        'restclients',
        'spotseeker_restclient'
        'userservice',
        'supporttools'
    )

MIDDLEWARE_CLASSES = (
        ...
        'django.contrib.auth.middleware.RemoteUserMiddleware',
        'userservice.user.UserServiceMiddleware'
    )

AUTHENTICATION_BACKENDS = (
        'django.contrib.auth.backends.RemoteUserBackend',
    )

USERSERVICE_ADMIN_GROUP = ''
AUTHZ_GROUP_BACKEND = 'authz_group.authz_implementation.all_ok.AllOK'


MANAGER_SUPERUSER_GROUP = 'u_acadev_tester' (or another mock group you define)
**Run with defined remote user, javerage will work with mock groups**
REMOTE_USER="javerage" ./manage runserver
 