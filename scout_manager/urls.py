from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    url(r'^$', 'scout_manager.views.home', name='home'),
    url(r'^test/', 'scout_manager.views.guidelines', name='guidelines'),

)