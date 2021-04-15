from .base_urls import *
from django.urls import include, re_path
from django.contrib import admin

urlpatterns += [
    re_path(r'^manager/', include('scout_manager.urls')),
]
