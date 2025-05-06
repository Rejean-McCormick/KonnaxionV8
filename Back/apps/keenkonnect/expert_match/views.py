# apps/keenkonnect/expert_match/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.expert_match.models import ExpertMatchRequest, CandidateProfile, MatchScore
from keenkonnect.expert_match.serializers import (
    ExpertMatchRequestSerializer,
    CandidateProfileSerializer,
    MatchScoreSerializer
)

logger = logging.getLogger(__name__)


class ExpertMatchRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les demandes de mise en relation avec des experts.
    """
    serializer_class = ExpertMatchRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']               # à ajuster selon votre modèle (ex. 'status', 'requester__username')
    search_fields = ['topic', 'description']    # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ExpertMatchRequest.objects.all()   # même logique que votre queryset initial
        logger.debug(
            "ExpertMatchRequest queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()            # conserve votre logique de création
        logger.info(
            "ExpertMatchRequest créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ExpertMatchRequestViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def trigger_match(self, request, pk=None):
        """
        Action personnalisée pour déclencher le processus de matching.
        (Ici, vous pouvez appeler une tâche asynchrone par exemple.)
        """
        match_request = self.get_object()
        try:
            # Exemple : déclencher la tâche asynchrone
            # trigger_expert_matching.delay(match_request.id)
            logger.info(
                "Matching déclenché pour ExpertMatchRequest id=%s par %s",
                match_request.id, request.user
            )
            return Response(
                {"status": "Matching déclenché", "match_request_id": match_request.id},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception(
                "Erreur lors du déclenchement du matching de %s par %s : %s",
                match_request.id, request.user, e
            )
            return Response(
                {"detail": "Impossible de déclencher le matching."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CandidateProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les profils candidats pour le matching.
    """
    serializer_class = CandidateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['expertise', 'location']  # à ajuster selon votre modèle
    search_fields = ['name', 'bio']               # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'rating']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = CandidateProfile.objects.all()       # même logique que votre queryset initial
        logger.debug(
            "CandidateProfile queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()              # conserve votre logique de création
        logger.info(
            "CandidateProfile créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CandidateProfileViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class MatchScoreViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour consulter et enregistrer les scores de compatibilité.
    """
    serializer_class = MatchScoreSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['match_request', 'candidate']  # à ajuster selon votre modèle
    ordering_fields = ['score', 'created_at']
    ordering = ['-score']

    def get_queryset(self):
        qs = MatchScore.objects.all()             # même logique que votre queryset initial
        logger.debug(
            "MatchScore queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()              # conserve votre logique de création
        logger.info(
            "MatchScore créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans MatchScoreViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
