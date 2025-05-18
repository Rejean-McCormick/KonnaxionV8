import logging

from rest_framework import viewsets, filters, status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ethikos.home.models import (
    DebateCategory,
    ResponseFormat,
    DebateTopic,
    FeaturedDebate,
    PersonalizedRecommendation,
    PublicVote,
)
from ethikos.home.serializers import (
    DebateCategorySerializer,
    ResponseFormatSerializer,
    DebateTopicSerializer,
    FeaturedDebateSerializer,
    PersonalizedRecommendationSerializer,
    PublicVoteSerializer,
)

logger = logging.getLogger(__name__)


class DebateCategoryViewSet(viewsets.ModelViewSet):
    """
    Gère les catégories de débat.
    - list/retrieve: utilisateurs authentifiés
    - create/update/delete: administrateurs
    """
    queryset = DebateCategory.objects.filter(is_deleted=False)
    serializer_class = DebateCategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['name']
    ordering = ['name']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info("DebateCategory créé (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("DebateCategory mis à jour (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_destroy(self, instance):
        logger.info("DebateCategory supprimé (id=%s) par %s", instance.pk, self.request.user)
        instance.delete()

    def handle_exception(self, exc):
        logger.exception("Erreur dans DebateCategoryViewSet pour %s : %s", self.request.user, exc)
        return super().handle_exception(exc)


class ResponseFormatViewSet(viewsets.ModelViewSet):
    """
    Gère les formats de réponse.
    - list/retrieve: utilisateurs authentifiés
    - create/update/delete: administrateurs
    """
    queryset = ResponseFormat.objects.filter(is_deleted=False)
    serializer_class = ResponseFormatSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'code']
    ordering_fields = ['id', 'name']
    ordering = ['id']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info("ResponseFormat créé (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("ResponseFormat mis à jour (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_destroy(self, instance):
        logger.info("ResponseFormat supprimé (id=%s) par %s", instance.pk, self.request.user)
        instance.delete()

    def handle_exception(self, exc):
        logger.exception("Erreur dans ResponseFormatViewSet pour %s : %s", self.request.user, exc)
        return super().handle_exception(exc)


class DebateTopicViewSet(viewsets.ModelViewSet):
    """
    Gère les sujets de débat.
    Accessible sans authentification en DEV.
    """
    queryset = DebateTopic.objects.all()
    serializer_class = DebateTopicSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['debatecategory', 'responseformat', 'is_active', 'is_deleted']
    search_fields = ['question', 'description']
    ordering_fields = ['created_at', 'question']
    ordering = ['question']

    def get_queryset(self):
        qs = super().get_queryset()
        logger.debug("DebateTopic queryset: %d items pour %s", qs.count(), self.request.user)
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info("DebateTopic créé (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("DebateTopic mis à jour (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_destroy(self, instance):
        logger.info("DebateTopic supprimé (id=%s) par %s", instance.pk, self.request.user)
        instance.delete()

    def handle_exception(self, exc):
        logger.exception("Erreur dans DebateTopicViewSet pour %s : %s", self.request.user, exc)
        return super().handle_exception(exc)


class FeaturedDebateViewSet(viewsets.ModelViewSet):
    """
    Gère les débats mis en avant.
    - list/retrieve: utilisateurs authentifiés
    - create/update/delete: administrateurs
    """
    serializer_class = FeaturedDebateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['topic__question']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = FeaturedDebate.objects.all()
        logger.debug("FeaturedDebate queryset: %d items pour %s", qs.count(), self.request.user)
        return qs

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info("FeaturedDebate créé (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info("FeaturedDebate mis à jour (id=%s) par %s", instance.pk, self.request.user)
        return instance

    def perform_destroy(self, instance):
        logger.info("FeaturedDebate supprimé (id=%s) par %s", instance.pk, self.request.user)
        instance.delete()

    def handle_exception(self, exc):
        logger.exception("Erreur dans FeaturedDebateViewSet pour %s : %s", self.request.user, exc)
        return super().handle_exception(exc)


class PersonalizedRecommendationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Lecture seule des recommandations personnalisées pour l'utilisateur connecté.
    """
    serializer_class = PersonalizedRecommendationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = PersonalizedRecommendation.objects.filter(user=self.request.user)
        logger.debug("PersonalizedRecommendation queryset: %d items pour %s", qs.count(), self.request.user)
        return qs

    def handle_exception(self, exc):
        logger.exception("Erreur dans PersonalizedRecommendationViewSet pour %s : %s", self.request.user, exc)
        return super().handle_exception(exc)


class PublicVoteViewSet(viewsets.ModelViewSet):
    """
    Enregistre un vote public sur un sujet.
    - list/retrieve: administrateurs
    - create: utilisateurs authentifiés
    """
    queryset = PublicVote.objects.all()
    serializer_class = PublicVoteSerializer
    http_method_names = ['get', 'post']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        logger.info("PublicVote créé (id=%s) topic=%s par %s", instance.pk, instance.topic_id, request.user)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def handle_exception(self, exc):
        logger.exception("Erreur dans PublicVoteViewSet pour %s : %s", self.request.user, exc)
        return super().handle_exception(exc)
