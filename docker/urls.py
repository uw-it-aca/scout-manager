# Copyright 2021 UW-IT, University of Washington
# SPDX-License-Identifier: Apache-2.0

from .base_urls import *
from django.urls import include, re_path
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns += [
    re_path(r"^manager/", include("scout_manager.urls")),
    # Redirects to /manager/spaces for /
    re_path(
        r"^$", RedirectView.as_view(url="/manager/spaces/")
    ),
]
