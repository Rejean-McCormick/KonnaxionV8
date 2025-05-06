from rest_framework import viewsets, permissions
from ethikos.stats.models import DebateStatistic, DebateEventLog
from ethikos.stats.serializers import (
    DebateStatisticSerializer,
    DebateEventLogSerializer
)

class DebateStatisticViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les statistiques des débats (ex. : nombre de votes, participants actifs).
    """
    serializer_class = DebateStatisticSerializer

    def get_queryset(self):
        # Liste globale : on ne filtre pas par utilisateur
        return DebateStatistic.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux admins
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class DebateEventLogViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour consulter et enregistrer les logs d'événements des débats.
    """
    serializer_class = DebateEventLogSerializer

    def get_queryset(self):
        # Logs globaux : on ne filtre pas par utilisateur
        return DebateEventLog.objects.all()

    def get_permissions(self):
        # Lecture pour tout utilisateur authentifié, écriture réservée aux admins
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]
