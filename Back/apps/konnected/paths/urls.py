# apps/konnected/paths/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.paths.views import (
    LearningPathViewSet,
    PathStepViewSet,
)

app_name = "paths"

router = DefaultRouter()
router.register(r"learning_paths", LearningPathViewSet, basename="learning_paths")
router.register(r"path_steps", PathStepViewSet, basename="path_steps")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
