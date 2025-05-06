# apps/konnaxion/core/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.core.views import (
    CustomUserViewSet,
    SystemConfigurationViewSet,
    ConfigurationChangeLogViewSet,
)

app_name = "core"

router = DefaultRouter()
router.register(r"users",                    CustomUserViewSet,             basename="customuser")
router.register(r"configurations",           SystemConfigurationViewSet,    basename="systemconfiguration")
router.register(r"configuration-changelogs", ConfigurationChangeLogViewSet, basename="configurationchangelog")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
