# apps/konnected/foundation/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.foundation.views import KnowledgeUnitViewSet

app_name = "foundation"

router = DefaultRouter()
router.register(
    r"knowledge_units",
    KnowledgeUnitViewSet,
    basename="knowledge_units"
)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
