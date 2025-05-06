from rest_framework import viewsets, permissions
from konnaxion.search.models import SearchIndex, SearchQueryLog
from konnaxion.search.serializers import SearchIndexSerializer, SearchQueryLogSerializer

class SearchIndexViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour gérer la configuration des index de recherche.
    """
    serializer_class = SearchIndexSerializer

    def get_queryset(self):
        # Tous les index, modifications réservées aux admins
        return SearchIndex.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAdminUser()]


class SearchQueryLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Endpoints en lecture seule pour consulter les journaux des requêtes de recherche.
    """
    serializer_class = SearchQueryLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les logs du user courant
        return SearchQueryLog.objects.filter(user=self.request.user)
