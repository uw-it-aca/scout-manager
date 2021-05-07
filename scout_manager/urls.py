# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from django.conf import settings
from django.urls import re_path
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from .views import pages
from scout_manager.views.api import Spot, SpotCreate, Item, ItemCreate

# from django.contrib import admin
# admin.autodiscover()

from django.contrib.auth.decorators import login_required

urlpatterns = [
    # /manager/
    re_path(
        r"^$", login_required(RedirectView.as_view(url="/manager/spaces/"))
    ),
    # /items/
    re_path(r"^items/$", login_required(pages.items), name="items"),
    re_path(
        r"^items/(?P<item_id>[0-9]{1,5})/$",
        login_required(pages.items_edit),
        name="items_edit",
    ),
    re_path(
        r"^items/add/$", login_required(pages.items_add), name="items_add"
    ),
    re_path(
        r"^items/add/batch/$",
        login_required(pages.items_add_batch),
        name="items_add_batch",
    ),
    # /spaces/
    re_path(r"^spaces/$", login_required(pages.spaces), name="spaces"),
    # /spaces/ID/
    re_path(
        r"^spaces/(?P<spot_id>[0-9]{1,5})/$",
        login_required(pages.spaces_edit),
        name="spaces_edit",
    ),
    # /spaces/ID/schedule/new/
    re_path(
        r"^spaces/(?P<spot_id>[0-9]{1,5})/schedule/new/$",
        login_required(pages.schedule),
        name="schedule",
    ),
    # /spaces/ID/schedule/DATETIME/
    re_path(
        r"^spaces/(?P<spot_id>[0-9]{1,5})/schedule/20160516/$",
        login_required(pages.schedule),
        name="schedule",
    ),
    # /spaces/add/
    re_path(
        r"^spaces/add/$", login_required(pages.spaces_add), name="spaces_add"
    ),
    # /spaces/add/
    re_path(
        r"^spaces/upload/$",
        login_required(pages.spaces_upload),
        name="spaces_upload",
    ),
    # /api/
    re_path(r"api/spot/(?P<spot_id>[0-9]{1,5})", login_required(Spot().run)),
    re_path(r"api/spot/", login_required(SpotCreate().run)),
    # /api/
    re_path(r"api/item/(?P<item_id>[0-9]{1,5})", login_required(Item().run)),
    re_path(r"api/item/", login_required(ItemCreate().run)),
    # manager spot image
    re_path(
        r"^images/(?P<spot_id>\d+)/image/(?P<image_id>\d+)/$",
        login_required(pages.image),
        name="manager_image",
    ),
    # manager item image
    re_path(
        r"^item/images/(?P<item_id>\d+)/image/(?P<image_id>\d+)/$",
        login_required(pages.item_image),
        name="manager_item_image",
    ),
]

# debug routes for developing error pages
if settings.DEBUG:
    urlpatterns += [
        re_path(r"^500/$", TemplateView.as_view(template_name="500.html")),
        re_path(r"^404/$", TemplateView.as_view(template_name="404.html")),
        re_path(r"^403/$", TemplateView.as_view(template_name="403.html")),
    ]
