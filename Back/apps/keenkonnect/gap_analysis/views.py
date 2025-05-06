# apps/keenkonnect/gap_analysis/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.gap_analysis.models import GapAnalysis
from keenkonnect.gap_analysis.serializers import GapAnalysisSerializer

logger = logging.getLogger(__name__)

class GapAnalysisViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les enregistrements d'analyse d'écart pour les projets.
    Permet de comparer le progrès prévu et réel et de stocker des recommandations.
    """
    serializer_class = GapAnalysisSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'project',      # à ajuster selon votre champ de relation vers le projet
        'status',       # ex. 'open', 'closed', etc.
    ]
    search_fields = [
        'title',        # à adapter si votre modèle utilise ce champ
        'recommendations',
    ]
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = GapAnalysis.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "GapAnalysis queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()   # conserve votre logique de création
        logger.info(
            "GapAnalysis créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans GapAnalysisViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
