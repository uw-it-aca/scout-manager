from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    url(r'^add/', 'scout_manager.views.add', name='add'),
    url(r'^item/', 'scout_manager.views.item', name='item'),
    url(r'^schedule/(?P<spot_id>[0-9]{1,5})', 'scout_manager.views.schedule', name='schedule'),
    url(r'^edit/(?P<spot_id>[0-9]{1,5})', 'scout_manager.views.edit', name='edit'),
    url(r'^test/', 'scout_manager.views.test', name='test'),
    url(r'^$', 'scout_manager.views.list', name='list'),

)
