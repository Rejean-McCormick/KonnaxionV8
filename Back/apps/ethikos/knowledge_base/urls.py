# apps/ethikos/knowledge_base/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.knowledge_base.views import DebateArchiveViewSet

app_name = "knowledge_base"

router = DefaultRouter()
router.register(r"debate_archives", DebateArchiveViewSet, basename="debate-archive")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
