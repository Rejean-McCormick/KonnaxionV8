from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.knowledge_hub.views import (
    KnowledgeDocumentViewSet,
    DocumentRevisionViewSet,
)

app_name = "knowledge_hub"

router = DefaultRouter()
router.register(
    r"knowledge_documents",
    KnowledgeDocumentViewSet,
    basename="knowledge-document",
)
router.register(
    r"document_revisions",
    DocumentRevisionViewSet,
    basename="document-revision",
)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
