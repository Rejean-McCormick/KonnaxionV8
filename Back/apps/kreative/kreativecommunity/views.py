# apps/konnected/konnectedcommunity/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from konnected.konnectedcommunity.models import DiscussionThread, Comment
from konnected.konnectedcommunity.serializers import (
    DiscussionThreadSerializer,
    CommentSerializer
)

logger = logging.getLogger(__name__)

class DiscussionThreadViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les fils de discussion (forum, Q&A) dans le cadre éducatif.
    """
    serializer_class = DiscussionThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']          # à ajuster selon vos champs
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = DiscussionThread.objects.all()       # même logique que votre queryset initial
        logger.debug(
            "DiscussionThread queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()               # conserve votre logique de création
        logger.info(
            "DiscussionThread créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DiscussionThreadViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class CommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires sur les discussions.
    """
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['thread']                 # à ajuster si besoin
    ordering = ['created_at']

    def get_queryset(self):
        qs = Comment.objects.all()                # même logique que votre queryset initial
        logger.debug(
            "Comment queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()               # conserve votre logique de création
        logger.info(
            "Comment créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CommentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
