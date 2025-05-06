# apps/konnected/foundation/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from konnected.foundation.models import KnowledgeUnit
from konnected.foundation.serializers import KnowledgeUnitSerializer

logger = logging.getLogger(__name__)

class KnowledgeUnitViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les Knowledge Units (contenu éducatif de base).
    """
    serializer_class = KnowledgeUnitSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['topic', 'is_active']    # à ajuster selon votre modèle (ex. 'topic', 'category', 'is_active', etc.)
    search_fields = ['title', 'description']     # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = KnowledgeUnit.objects.all()          # même logique que votre queryset initial
        logger.debug(
            "KnowledgeUnit queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()              # conserve votre logique de création
        logger.info(
            "KnowledgeUnit créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans KnowledgeUnitViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
