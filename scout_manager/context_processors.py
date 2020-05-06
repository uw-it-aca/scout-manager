from django.conf import settings

def manager_mail_to(request):
    mail_to_email = getattr(settings, 'MANAGER_MAIL_TO_EMAIL', False)
    return {
        'MAIL_TO_EMAIL': mail_to_email
    }
