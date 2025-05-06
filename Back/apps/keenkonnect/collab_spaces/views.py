# apps/keenkonnect/collab_spaces/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from keenkonnect.collab_spaces.models import CollabSpace, Document, ChatMessage
from keenkonnect.collab_spaces.serializers import (
    CollabSpaceSerializer,
    DocumentSerializer,
    ChatMessageSerializer
)
# Si vous utilisez une tâche Celery pour notifier en temps réel, décommentez :
# from keenkonnect.collab_spaces.tasks import notify_new_chat_message

logger = logging.getLogger(__name__)


class CollabSpaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les espaces de collaboration.
    """
    serializer_class = CollabSpaceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['participants']              # À ajuster selon votre modèle
    search_fields = ['name', 'description']          # À adapter aux champs réels
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = CollabSpace.objects.filter(participants=self.request.user)
        logger.debug(
            "CollabSpace queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        collab_space = serializer.save()
        collab_space.participants.add(self.request.user)
        logger.info(
            "CollabSpace créé (id=%s) par %s",
            collab_space.pk, self.request.user
        )
        return collab_space

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def add_participant(self, request, pk=None):
        """
        Ajoute un participant (user_id dans request.data) à l’espace.
        """
        collab_space = self.get_object()
        user_id = request.data.get('user_id')
        if not user_id:
            logger.warning("add_participant sans user_id par %s", request.user)
            return Response(
                {"error": "Le champ 'user_id' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            collab_space.participants.add(user_id)
            logger.info(
                "Utilisateur %s ajouté à CollabSpace id=%s par %s",
                user_id, collab_space.pk, request.user
            )
            return Response(self.get_serializer(collab_space).data, status=status.HTTP_200_OK)
        except Exception as exc:
            logger.exception(
                "Erreur add_participant pour CollabSpace id=%s par %s: %s",
                collab_space.pk, request.user, exc
            )
            return Response(
                {"error": str(exc)},
                status=status.HTTP_400_BAD_REQUEST
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CollabSpaceViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class DocumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les documents partagés dans un espace de collaboration.
    """
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collab_space']               # À ajuster selon votre modèle
    search_fields = ['title', 'filename']             # À adapter aux champs réels
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = Document.objects.filter(collab_space__participants=self.request.user)
        logger.debug(
            "Document queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        doc = serializer.save()
        logger.info(
            "Document créé (id=%s) par %s",
            doc.pk, self.request.user
        )
        return doc

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DocumentViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ChatMessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les messages de chat dans un espace de collaboration.
    """
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['collab_space', 'sender']     # À ajuster selon votre modèle
    search_fields = ['message']                       # À adapter au champ réel
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        qs = ChatMessage.objects.filter(collab_space__participants=self.request.user)
        logger.debug(
            "ChatMessage queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        logger.info(
            "ChatMessage créé (id=%s) par %s",
            message.pk, self.request.user
        )
        # Si notification en temps réel :
        # notify_new_chat_message.delay(message.id)
        return message

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        """
        Marque un message comme lu.
        """
        message = self.get_object()
        try:
            message.is_read = True
            message.save()
            logger.info(
                "ChatMessage id=%s marqué comme lu par %s",
                message.pk, request.user
            )
            return Response(self.get_serializer(message).data, status=status.HTTP_200_OK)
        except Exception as exc:
            logger.exception(
                "Erreur dans mark_as_read pour ChatMessage id=%s par %s: %s",
                message.pk, request.user, exc
            )
            return Response(
                {"detail": "Impossible de marquer le message comme lu."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ChatMessageViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
