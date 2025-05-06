# apps/ethikos/resolution/views.py

from rest_framework import viewsets, permissions
from ethikos.resolution.models import DebateResolution
from ethikos.resolution.serializers import DebateResolutionSerializer

class DebateResolutionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les résolutions de débats.
    Chaque résolution inclut l'audit trail complet des décisions.
    """
    serializer_class = DebateResolutionSerializer

    def get_queryset(self):
        # Toutes les résolutions sont visibles, la logique métier peut filtrer si nécessaire
        return DebateResolution.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux administrateurs
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
