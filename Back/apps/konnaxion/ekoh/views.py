# apps/konnaxion/ekoh/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from konnaxion.ekoh.models import (
    ExpertiseTag,
    ReputationProfile,
    ReputationEvent,
    WeightedVote
)
from konnaxion.ekoh.serializers import (
    ExpertiseTagSerializer,
    ReputationProfileSerializer,
    ReputationEventSerializer,
    WeightedVoteSerializer
)
# Exemple : Importer une tâche pour recalculer la réputation
# from konnaxion.ekoh.tasks import recalculate_reputation

logger = logging.getLogger(__name__)


class ExpertiseTagViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour gérer les tags d'expertise.
    """
    serializer_class = ExpertiseTagSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = []               # à ajuster (ex. 'category', 'is_active', etc.)
    search_fields = ['name']            # à adapter selon votre modèle
    ordering_fields = ['created_at']    # à ajuster si vous avez un champ date
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ExpertiseTag.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ExpertiseTag queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "ExpertiseTag créé (id=%s) par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ExpertiseTagViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ReputationProfileViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour consulter et mettre à jour le profil de réputation des utilisateurs.
    """
    serializer_class = ReputationProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user']             # à ajuster (ex. 'score_range', etc.)
    ordering_fields = ['score', 'updated_at']
    ordering = ['-score']

    def get_queryset(self):
        qs = ReputationProfile.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ReputationProfile queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "ReputationProfile créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "ReputationProfile mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ReputationProfileViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ReputationEventViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints en lecture seule pour consulter les événements impactant la réputation.
    """
    serializer_class = ReputationEventSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['user', 'event_type']  # à ajuster selon votre modèle
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = ReputationEvent.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "ReputationEvent queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ReputationEventViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class WeightedVoteViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des votes pondérés.
    À la création d'un vote, un recalcul asynchrone de la réputation peut être déclenché.
    """
    serializer_class = WeightedVoteSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'target']      # à ajuster selon votre modèle
    search_fields = []                         # ex. ['comment']
    ordering_fields = ['vote_value', 'created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = WeightedVote.objects.all()       # même logique que votre queryset initial
        logger.debug(
            "WeightedVote queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        vote = serializer.save()
        logger.info(
            "WeightedVote créé (id=%s, value=%s) par %s",
            vote.pk, vote.vote_value, self.request.user
        )
        # Exemple : Déclencher la tâche asynchrone de recalcul de réputation
        # recalculate_reputation.delay(vote.user.id, vote.target_id, vote.vote_value)

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans WeightedVoteViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
