# apps/kreative/immersive/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from kreative.immersive.models import ImmersiveExperience
from kreative.immersive.serializers import ImmersiveExperienceSerializer

logger = logging.getLogger(__name__)

class ImmersiveExperienceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les expériences immersives (AR/VR).
    Ce module est minimal et peut être étendu ultérieurement.
    """
    serializer_class = ImmersiveExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []                       # à ajuster selon vos champs (ex. 'category', 'is_active', etc.)
    search_fields = ['title', 'description']    # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ImmersiveExperience.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ImmersiveExperience queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()            # conserve votre logique de création
        logger.info(
            "ImmersiveExperience créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ImmersiveExperienceViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
