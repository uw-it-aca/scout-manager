from django.conf import settings
from django.conf.urls import url
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from .views import pages
from scout_manager.views.api import Spot, SpotCreate,\
    Item, ItemCreate
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    # /manager/
    url(r'^$', RedirectView.as_view(url='/manager/spaces/')),

    # /items/
    url(r'^items/$', pages.items,
        name='items'),

    url(r'^items/(?P<item_id>[0-9]{1,5})/$',
        pages.items_edit,
        name='items_edit'),

    url(r'^items/add/$',
        pages.items_add,
        name='items_add'),

    url(r'^items/add/batch/$',
        pages.items_add_batch,
        name='items_add_batch'),

    # /spaces/
    url(r'^spaces/$',
        pages.spaces,
        name='spaces'),

    # /spaces/ID/
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})/$',
        pages.spaces_edit,
        name='spaces_edit'),

    # /spaces/ID/schedule/new/
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})/schedule/new/$',
        pages.schedule,
        name='schedule'),

    # /spaces/ID/schedule/DATETIME/
    url(r'^spaces/(?P<spot_id>[0-9]{1,5})/schedule/20160516/$',
        pages.schedule,
        name='schedule'),

    # /spaces/add/
    url(r'^spaces/add/$',
        pages.spaces_add,
        name='spaces_add'),

    # /spaces/add/
    url(r'^spaces/upload/$',
        pages.spaces_upload,
        name='spaces_upload'),

    # /api/
    url(r'api/spot/(?P<spot_id>[0-9]{1,5})',
        Spot().run),

    url(r'api/spot/',
        SpotCreate().run),

    # /api/
    url(r'api/item/(?P<item_id>[0-9]{1,5})',
        Item().run),

    url(r'api/item/',
        ItemCreate().run),

    # manager spot image
    url(r'^images/(?P<spot_id>\d+)/image/(?P<image_id>\d+)/$',
        pages.image,
        name='manager_image'),

    # manager item image
    url(r'^item/images/(?P<item_id>\d+)/image/(?P<image_id>\d+)/$',
        pages.item_image,
        name='manager_item_image'),
]

# debug routes for developing error pages
if settings.DEBUG:
    urlpatterns += [
        url(r'^500/$', TemplateView.as_view(template_name='500.html')),
        url(r'^404/$', TemplateView.as_view(template_name='404.html')),
        url(r'^403/$', TemplateView.as_view(template_name='403.html')),
    ]
