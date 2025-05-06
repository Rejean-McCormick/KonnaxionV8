# apps/konnaxion/core/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from konnaxion.core.models import (
    CustomUser,
    SystemConfiguration,
    ConfigurationChangeLog
)
from konnaxion.core.serializers import (
    CustomUserSerializer,
    SystemConfigurationSerializer,
    ConfigurationChangeLogSerializer
)
# Exemple : Importer une tâche asynchrone pour consigner les changements de configuration
# from konnaxion.core.tasks import log_configuration_change

logger = logging.getLogger(__name__)


class CustomUserViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des utilisateurs (CustomUser).
    """
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['is_active', 'role', 'email']      # à ajuster selon vos champs
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['date_joined', 'last_login']
    ordering = ['-date_joined']

    def get_queryset(self):
        qs = CustomUser.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "CustomUser queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        user = serializer.save()
        logger.info(
            "CustomUser créé (id=%s) par %s",
            user.pk, self.request.user
        )

    def perform_update(self, serializer):
        user = serializer.save()
        logger.info(
            "CustomUser mis à jour (id=%s) par %s",
            user.pk, self.request.user
        )
        return user

    def perform_destroy(self, instance):
        logger.info(
            "CustomUser supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_profile(self, request, pk=None):
        """
        Action personnalisée pour mettre à jour le profil utilisateur.
        (Ici, vous pouvez déclencher un événement asynchrone pour la synchronisation offline ou la notification.)
        """
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)
        try:
            serializer.is_valid(raise_exception=True)
            updated = serializer.save()
            # Exemple : tasks.trigger_user_update_event.delay(updated.id)
            logger.info(
                "Profil utilisateur mis à jour via update_profile (id=%s) par %s",
                updated.pk, request.user
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as exc:
            logger.exception(
                "Erreur dans update_profile pour %s: %s",
                request.user, exc
            )
            return Response(
                {"detail": "Impossible de mettre à jour le profil."},
                status=status.HTTP_400_BAD_REQUEST
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans CustomUserViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class SystemConfigurationViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion de la configuration système.
    Toute modification peut déclencher un enregistrement asynchrone dans l’historique.
    """
    serializer_class = SystemConfigurationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['key', 'environment']  # à ajuster selon vos champs
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']

    def get_queryset(self):
        qs = SystemConfiguration.objects.all()
        logger.debug(
            "SystemConfiguration queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        cfg = serializer.save()
        logger.info(
            "SystemConfiguration créé (id=%s) par %s",
            cfg.pk, self.request.user
        )

    def perform_update(self, serializer):
        cfg = serializer.save()
        logger.info(
            "SystemConfiguration mis à jour (id=%s) par %s",
            cfg.pk, self.request.user
        )
        # Exemple : log_configuration_change.delay(cfg.id)
        return cfg

    def perform_destroy(self, instance):
        logger.info(
            "SystemConfiguration supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans SystemConfigurationViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ConfigurationChangeLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoint en lecture seule pour consulter l’historique des modifications de configuration.
    """
    serializer_class = ConfigurationChangeLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['configuration', 'user']
    ordering_fields = ['action_time']
    ordering = ['-action_time']

    def get_queryset(self):
        qs = ConfigurationChangeLog.objects.all()
        logger.debug(
            "ConfigurationChangeLog queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ConfigurationChangeLogViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
