# apps/ethikos/prioritization/views.py
from rest_framework import viewsets, permissions
from ethikos.prioritization.models import DebatePrioritization
from ethikos.prioritization.serializers import DebatePrioritizationSerializer

class DebatePrioritizationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer le classement et le filtrage des débats.
    Les critères d'engagement et de crédibilité sont pris en compte dans le score.
    """
    serializer_class = DebatePrioritizationSerializer

    def get_queryset(self):
        # Toutes les priorisations sont visibles
        return DebatePrioritization.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux admins
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
