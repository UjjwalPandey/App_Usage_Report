from django.conf.urls import url, include
from rest_framework import routers

from . import views

app_name = "report"

router = routers.DefaultRouter()
router.register(r'report', views.ReportViewSet, basename="report")

urlpatterns = [
    url(r'^', include(router.urls)),
]
