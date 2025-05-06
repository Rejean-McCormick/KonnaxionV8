# apps/keenkonnect/knowledge_hub/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.knowledge_hub.views import (
    KnowledgeDocumentViewSet,
    DocumentRevisionViewSet,
)

app_name = "knowledge_hub"

router = DefaultRouter()
router.register(r"knowledge_documents",  KnowledgeDocumentViewSet)
router.register(r"document_revisions",    DocumentRevisionViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
