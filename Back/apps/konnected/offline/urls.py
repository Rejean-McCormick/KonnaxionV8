# apps/konnected/offline/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.offline.views import OfflineContentPackageViewSet

app_name = "offline"

router = DefaultRouter()
router.register(r"offline_packages", OfflineContentPackageViewSet, basename="offlinepackage")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
