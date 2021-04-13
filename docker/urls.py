from django.urls import include, re_path
from django.contrib import admin

urlpatterns = [
    re_path(r'^manager/', include('scout_manager.urls')),
    re_path(r'^', include('project.base_urls')),
]
