from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^manager/', include('scout_manager.urls')),
    url(r'^', include('django_prometheus.urls')), # add here for django 1.11 compatibility
    url(r'^saml/', include('uw_saml.urls')),  # add here for django 1.11 compatibility
]
