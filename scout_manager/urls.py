from django.conf.urls import patterns, include, url

# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    # /manager/
    url(r'^$', 'scout_manager.views.home', name='home'),

    # /items/
    url(r'^items/$', 'scout_manager.views.items', name='items'),
    url(r'^items/(?P<item_id>[0-9]{1,5})', 'scout_manager.views.items_edit', name='items_edit'),
    url(r'^items/add/', 'scout_manager.views.items_add', name='items_add'),

    # /spaces/
    url(r'^spaces/$', 'scout_manager.views.spaces', name='spaces'),
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})', 'scout_manager.views.spaces_edit', name='spaces_edit'),
    url(r'^spaces/add/', 'scout_manager.views.spaces_add', name='spaces_add'),

    url(r'^schedule/(?P<spot_id>[0-9]{1,5})', 'scout_manager.views.schedule', name='schedule'),

)
