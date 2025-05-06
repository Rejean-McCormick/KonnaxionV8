# apps/kreative/artworks/views.py

import logging

from rest_framework import viewsets, permissions, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from kreative.artworks.models import Exhibition, Artwork
from kreative.artworks.serializers import ExhibitionSerializer, ArtworkSerializer

logger = logging.getLogger(__name__)


class ExhibitionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les expositions (création, modification, suppression et consultation).
    """
    serializer_class = ExhibitionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active', 'location']      # ajuster selon vos champs réels
    search_fields = ['title', 'description']
    ordering_fields = ['start_date', 'end_date', 'created_at']
    ordering = ['-start_date']

    def get_queryset(self):
        qs = Exhibition.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "Exhibition queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "Exhibition créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "Exhibition mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "Exhibition supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def activate(self, request, pk=None):
        """
        Action personnalisée pour activer/désactiver une exposition.
        Attendu : un booléen 'active' dans request.data.
        """
        exhibition = self.get_object()
        active = request.data.get('active')
        if active is None:
            logger.warning("activate sans paramètre 'active' par %s", request.user)
            return Response(
                {"error": "Le champ 'active' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            exhibition.active = bool(active)
            exhibition.save()
            logger.info(
                "Exhibition (id=%s) active=%s mise à jour par %s",
                exhibition.pk, exhibition.active, request.user
            )
            return Response(
                self.get_serializer(exhibition).data,
                status=status.HTTP_200_OK
            )
        except Exception as exc:
            logger.exception(
                "Erreur dans activate pour Exhibition id=%s par %s: %s",
                exhibition.pk, request.user, exc
            )
            return Response(
                {"detail": "Impossible de changer le statut de l'exposition."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ExhibitionViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)


class ArtworkViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer le catalogue des œuvres.
    """
    serializer_class = ArtworkSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['exhibition', 'artist']    # ajuster selon vos champs
    search_fields = ['title', 'medium']
    ordering_fields = ['created_at', 'year']
    ordering = ['created_at']

    def get_queryset(self):
        qs = Artwork.objects.all()  # même logique que votre queryset initial
        logger.debug(
            "Artwork queryset: %d items pour %s",
            qs.count(), self.request.user
        )
        return qs

    def perform_create(self, serializer):
        instance = serializer.save()
        logger.info(
            "Artwork créé (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_update(self, serializer):
        instance = serializer.save()
        logger.info(
            "Artwork mis à jour (id=%s) par %s",
            instance.pk, self.request.user
        )
        return instance

    def perform_destroy(self, instance):
        logger.info(
            "Artwork supprimé (id=%s) par %s",
            instance.pk, self.request.user
        )
        instance.delete()

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def by_exhibition(self, request):
        """
        Retourne la liste des œuvres filtrées par l'exposition.
        Expects : un paramètre 'exhibition_id' dans les query params.
        """
        exhibition_id = request.query_params.get('exhibition_id')
        qs = self.get_queryset()
        if exhibition_id:
            qs = qs.filter(exhibition_id=exhibition_id)
        logger.debug(
            "by_exhibition: %d artworks pour exhibition_id=%s par %s",
            qs.count(), exhibition_id, request.user
        )
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    def handle_exception(self, exc):
        logger.exception(
            "Erreur dans ArtworkViewSet pour %s: %s",
            self.request.user, exc
        )
        return super().handle_exception(exc)
