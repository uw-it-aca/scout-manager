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
    )

    TEMPLATES = [
        {
            'OPTIONS': {
                'context_processors': [
                    ...
                    'scout_manager.context_processors.is_branded',
                ],
            },
        },
    ]

    #scout manager
    SCOUT_MGR_BRANDING = True
