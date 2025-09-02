# ip_tracking/urls.py
from django.urls import path

from ip_tracking.views import TestGeoLocationView

urlpatterns = [
    path("test-geo/", TestGeoLocationView.as_view(), name="test_geo"),
]
