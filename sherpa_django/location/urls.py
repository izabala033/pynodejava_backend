from django.conf.urls import url, include
from django.urls import path
from rest_framework import routers

# Register API Endpoints
from location.views import LocationViewSet
router = routers.SimpleRouter()
router.register('location', LocationViewSet, basename='location')

urlpatterns = [
    url(r'^', include(router.urls)),
]
