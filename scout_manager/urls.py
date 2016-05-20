from django.conf.urls import patterns, url
from scout_manager.views.api import Spot
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:

    # /manager/
    url(r'^$', 'scout_manager.views.pages.home',
        name='home'),

    # /items/
    url(r'^items/$', 'scout_manager.views.pages.items',
        name='items'),

    url(r'^items/(?P<item_id>[0-9]{1,5})/$',
        'scout_manager.views.pages.items_edit',
        name='items_edit'),

    url(r'^items/add/$',
        'scout_manager.views.pages.items_add',
        name='items_add'),

    # /unpublished/
    url(r'^unpublished/$',
        'scout_manager.views.pages.unpublished',
        name='unpublished'),

    # /spaces/
    url(r'^spaces/$',
        'scout_manager.views.pages.spaces',
        name='spaces'),

    # /spaces/ID/
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})/$',
        'scout_manager.views.pages.spaces_edit',
        name='spaces_edit'),

    # /spaces/ID/schedule/new/
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})/schedule/new/$',
        'scout_manager.views.pages.schedule',
        name='schedule'),

    # /spaces/ID/schedule/DATETIME/
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})/schedule/20160516/$',
        'scout_manager.views.pages.schedule',
        name='schedule'),

    # /spaces/add/
    url(r'^spaces/add/$',
        'scout_manager.views.pages.spaces_add',
        name='spaces_add'),

    # /api/
    url(r'api/spot/(?P<spot_id>[0-9]{1,5})',
        Spot().run)

)
