# apps/ethikos/home/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from ethikos.home.models import DebateTopic, FeaturedDebate, PersonalizedRecommendation
from ethikos.home.serializers import (
    DebateTopicSerializer,
    FeaturedDebateSerializer,
    PersonalizedRecommendationSerializer
)

logger = logging.getLogger(__name__)


class DebateTopicViewSet(viewsets.ModelViewSet):
    """
    Gère les sujets de débat.
    - List & Retrieve : tout utilisateur authentifié
    - Create/Update/Delete : uniquement les administrateurs
    """
    serializer_class = DebateTopicSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']            # à ajuster selon votre modèle (ex. 'category', 'is_active', etc.)
    search_fields = ['title']                  # à adapter aux champs de votre modèle
    ordering_fields = ['created_at', 'title']
    ordering = ['title']

    def get_queryset(self):
        qs = DebateTopic.objects.all()         # même logique que votre queryset initial
        logger.debug(
            "DebateTopic queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()            # conserve votre logique de création
        logger.info(
            "DebateTopic créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "DebateTopic mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "DebateTopic supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DebateTopicViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class FeaturedDebateViewSet(viewsets.ModelViewSet):
    """
    Gère les débats mis en avant.
    - List & Retrieve : tout utilisateur authentifié
    - Create/Update/Delete : uniquement les administrateurs
    """
    serializer_class = FeaturedDebateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']            # à ajuster selon votre modèle
    search_fields = ['topic__title']           # ou un autre champ pertinent
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = FeaturedDebate.objects.all()      # même logique que votre queryset initial
        logger.debug(
            "FeaturedDebate queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "FeaturedDebate créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "FeaturedDebate mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "FeaturedDebate supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans FeaturedDebateViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class PersonalizedRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lecture seule des recommandations personnalisées pour l'utilisateur connecté.
    """
    serializer_class = PersonalizedRecommendationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = PersonalizedRecommendation.objects.filter(user=self.request.user)
        logger.debug(
            "PersonalizedRecommendation queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans PersonalizedRecommendationViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
