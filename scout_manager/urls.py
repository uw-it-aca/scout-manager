from django.conf.urls import patterns, include, url
from scout_manager.views.api import Spot
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    # /manager/
    url(r'^$', 'scout_manager.views.pages.home', name='home'),

    # /items/
    url(r'^items/$', 'scout_manager.views.pages.items', name='items'),
    url(r'^items/(?P<item_id>[0-9]{1,5})/$', 'scout_manager.views.pages.items_edit', name='items_edit'),
    url(r'^items/add/$', 'scout_manager.views.pages.items_add', name='items_add'),

    # /spaces/
    url(r'^spaces/$', 'scout_manager.views.pages.spaces', name='spaces'),
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})/$', 'scout_manager.views.pages.spaces_edit', name='spaces_edit'),
    url(r'^spaces/add/$', 'scout_manager.views.pages.spaces_add', name='spaces_add'),

    # /schedule/
    url(r'^schedule/(?P<spot_id>[0-9]{1,5})', 'scout_manager.views.pages.schedule', name='schedule'),

    url(r'api/spot/(?P<spot_id>[0-9]{1,5})', Spot().run)

)
