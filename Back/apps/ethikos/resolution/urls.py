# apps/ethikos/resolution/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.resolution.views import DebateResolutionViewSet

app_name = "resolution"

router = DefaultRouter()
router.register(
    r"debate_resolutions",
    DebateResolutionViewSet,
    basename="debateresolution"
)

urlpatterns = [
    path(
        "",
        include((router.urls, app_name), namespace=app_name)
    ),
]
