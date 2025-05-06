from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from kreative.marketplace.models import ArtistProfile, Commission, MarketplaceListing
from kreative.marketplace.serializers import (
    ArtistProfileSerializer,
    CommissionSerializer,
    MarketplaceListingSerializer
)

class ArtistProfileViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les profils d'artistes.
    Permet aux artistes de gérer leur profil et leur portfolio.
    """
    serializer_class = ArtistProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que le profil de l'artiste connecté
        return ArtistProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement le profil à l'utilisateur
        serializer.save(user=self.request.user)


class CommissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les commissions artistiques.
    Permet de créer, mettre à jour et suivre les demandes de commissions.
    """
    serializer_class = CommissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les commissions créées par l'utilisateur
        return Commission.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement la commission à l'utilisateur
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def update_status(self, request, pk=None):
        """
        Action personnalisée pour mettre à jour le statut d'une commission.
        """
        commission = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response(
                {"error": "Le champ 'status' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )
        commission.status = new_status
        commission.save()
        return Response(self.get_serializer(commission).data)


class MarketplaceListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les annonces du marketplace.
    Permet de créer, mettre à jour et supprimer des annonces d'œuvres ou de commissions.
    """
    serializer_class = MarketplaceListingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les annonces créées par l'utilisateur
        return MarketplaceListing.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement l'annonce à l'utilisateur
        serializer.save(created_by=self.request.user)
