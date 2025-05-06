# apps/kreative/immersive/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kreative.immersive.views import ImmersiveExperienceViewSet

app_name = "immersive"

router = DefaultRouter()
router.register(r"immersive_experiences", ImmersiveExperienceViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
