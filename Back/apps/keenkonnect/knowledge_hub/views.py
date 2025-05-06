# apps/keenkonnect/knowledge_hub/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.knowledge_hub.models import KnowledgeDocument, DocumentRevision
from keenkonnect.knowledge_hub.serializers import (
    KnowledgeDocumentSerializer,
    DocumentRevisionSerializer
)
# Exemple : Importer une tâche asynchrone pour gérer la révision de document
# from keenkonnect.knowledge_hub.tasks import trigger_document_revision

logger = logging.getLogger(__name__)

class KnowledgeDocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les documents du Knowledge Hub.
    """
    serializer_class = KnowledgeDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']            # à ajuster si vous avez un champ 'status'
    search_fields = ['title', 'content']     # à ajuster selon vos champs
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = KnowledgeDocument.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "KnowledgeDocument queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()           # conserve votre logique de création
        logger.info(
            "KnowledgeDocument créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans KnowledgeDocumentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def revise(self, request, pk=None):
        """
        Action personnalisée pour lancer une révision du document.
        """
        document = self.get_object()
        try:
            # Exemple : déclencher une tâche asynchrone de révision
            # trigger_document_revision.delay(document.id)
            logger.info(
                "Révision déclenchée pour KnowledgeDocument id=%s par %s",
                document.id, request.user
            )
            return Response(
                {"status": "Révision déclenchée", "document_id": document.id},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception(
                "Erreur lors de la révision de %s par %s : %s",
                document.id, request.user, e
            )
            return Response(
                {"detail": "Impossible de lancer la révision."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class DocumentRevisionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les révisions des documents.
    """
    serializer_class = DocumentRevisionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['document']         # à ajuster si besoin
    ordering = ['created_at']

    def get_queryset(self):
        qs = DocumentRevision.objects.all()   # même logique que votre queryset initial
        logger.debug(
            "DocumentRevision queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()           # conserve votre logique de création
        logger.info(
            "DocumentRevision créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DocumentRevisionViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
