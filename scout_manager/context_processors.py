from django.conf import settings

def is_branded(request):

    brandedapp = getattr(settings, 'SCOUT_MGR_BRANDING', False)
    return {
        'SCOUT_MGR_BRANDING': brandedapp,
        'is_branded': brandedapp
    }
