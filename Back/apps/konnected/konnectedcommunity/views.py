# apps/konnected/konnectedcommunity/views.py

import logging

from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend

from konnected.konnectedcommunity.models import DiscussionThread, Comment
from konnected.konnectedcommunity.serializers import (
    DiscussionThreadSerializer,
    CommentSerializer
)
from kreative.kreativecommunity.models import CommunityPost, PostComment
from kreative.kreativecommunity.serializers import (
    CommunityPostSerializer,
    PostCommentSerializer
)

logger = logging.getLogger(__name__)


class DiscussionThreadViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les fils de discussion (forum, Q&A) dans le cadre éducatif.
    """
    serializer_class = DiscussionThreadSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'author__username']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = DiscussionThread.objects.filter(is_active=True)
        logger.debug(
            "DiscussionThread queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
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
    filterset_fields = ['thread', 'parent']
    ordering = ['created_at']

    def get_queryset(self):
        qs = Comment.objects.filter(thread__is_active=True)
        logger.debug(
            "Comment queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
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


class CommunityPostViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les posts communautaires autour des arts.
    """
    serializer_class = CommunityPostSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_public', 'author__username']
    search_fields = ['title', 'body']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = CommunityPost.objects.filter(is_public=True)
        logger.debug(
            "CommunityPost queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            "CommunityPost créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CommunityPostViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class PostCommentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commentaires sur les posts communautaires.
    """
    serializer_class = PostCommentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post']
    ordering = ['created_at']

    def get_queryset(self):
        qs = PostComment.objects.filter(post__is_public=True)
        logger.debug(
            "PostComment queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user)
        logger.info(
            "PostComment créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans PostCommentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
