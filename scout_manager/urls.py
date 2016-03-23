from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    url(r'^add/', 'scout_manager.views.add', name='add'),
    url(r'^item/', 'scout_manager.views.item', name='item'),
    url(r'^future/', 'scout_manager.views.future', name='future'),
    url(r'^space/', 'scout_manager.views.space', name='space'),
    url(r'^test/', 'scout_manager.views.test', name='test'),
    url(r'^$', 'scout_manager.views.list', name='list'),

)
