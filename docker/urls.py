from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^manager/', include('scout_manager.urls')),
    url(r'^', include('django_prometheus.urls')), # add here for django 1.11 compatibility
]
