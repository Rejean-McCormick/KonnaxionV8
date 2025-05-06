# apps/ethikos/knowledge_base/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ethikos.knowledge_base.models import DebateArchive
from ethikos.knowledge_base.serializers import DebateArchiveSerializer

logger = logging.getLogger(__name__)

class DebateArchiveViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer l'archivage des débats et des contenus de référence.
    """
    serializer_class = DebateArchiveSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['year']             # à ajuster selon vos champs métier
    search_fields = ['title', 'summary']    # à ajuster selon vos champs
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = DebateArchive.objects.all()   # même logique que votre queryset initial
        logger.debug(
            "DebateArchive queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()        # conserve votre logique de création
        logger.info(
            "DebateArchive créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DebateArchiveViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
