# apps/ethikos/debate_arena/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from ethikos.debate_arena.models import DebateSession, Argument, VoteRecord
from ethikos.debate_arena.serializers import (
    DebateSessionSerializer,
    ArgumentSerializer,
    VoteRecordSerializer
)

logger = logging.getLogger(__name__)


class DebateSessionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les sessions de débat en temps réel.
    """
    serializer_class = DebateSessionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'topic']           # à ajuster selon vos champs
    search_fields = ['title', 'description']            # à adapter aux champs de votre modèle
    ordering_fields = ['start_time', 'end_time']
    ordering = ['-start_time']

    def get_queryset(self):
        qs = DebateSession.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "DebateSession queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()       # conserve votre logique de création
        logger.info(
            "DebateSession créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans DebateSessionViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def end_session(self, request, pk=None):
        """
        Action pour clôturer une session de débat.
        Met à jour `is_active` et éventuellement `end_time`.
        """
        session = self.get_object()
        try:
            session.is_active = False
            # si end_time est fourni, sinon il reste inchangé
            if 'end_time' in request.data:
                session.end_time = request.data['end_time']
            session.save()
            logger.info(
                "DebateSession (id=%s) clôturée par %s",
                session.pk, request.user
            )
            return Response(
                self.get_serializer(session).data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            logger.exception(
                "Erreur lors de la clôture de la session %s par %s: %s",
                session.pk, request.user, e
            )
            return Response(
                {"detail": "Impossible de clôturer la session."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ArgumentViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les arguments dans une session de débat.
    """
    serializer_class = ArgumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['session', 'author']             # à ajuster selon vos champs
    search_fields = ['text']                             # à adapter au champ d’argument
    ordering_fields = ['created_at']
    ordering = ['created_at']

    def get_queryset(self):
        qs = Argument.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "Argument queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()  # conserve votre logique de création
        logger.info(
            "Argument créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ArgumentViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class VoteRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer l'enregistrement des votes sur les arguments.
    """
    serializer_class = VoteRecordSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['argument', 'voter']            # à ajuster selon vos champs
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = VoteRecord.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "VoteRecord queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()  # conserve votre logique de création
        logger.info(
            "VoteRecord créé (id=%s) via API par %s",
            instance.pk, self.request.user
        )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans VoteRecordViewSet pour %s : %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
