from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = "zoom"

router = routers.DefaultRouter()
router.register(r'zoom', views.ZoomViewSet, basename="zoom")

urlpatterns = [
    url(r'^', include(router.urls)),
]
