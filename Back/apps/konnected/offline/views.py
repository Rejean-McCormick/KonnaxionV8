# apps/konnected/offline/views.py

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from konnected.offline.models import OfflineContentPackage
from konnected.offline.serializers import OfflineContentPackageSerializer
# Exemple : depuis un module de tâches asynchrones pour lancer la synchronisation
# from konnected.offline.tasks import sync_offline_content

class OfflineContentPackageViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les packages de contenu pour l'utilisation offline.
    """
    queryset = OfflineContentPackage.objects.all()
    serializer_class = OfflineContentPackageSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def sync(self, request, pk=None):
        """
        Action personnalisée pour déclencher la synchronisation du package offline.
        """
        package = self.get_object()
        # Exemple : déclencher la tâche asynchrone de synchronisation
        # sync_offline_content.delay(package.id)
        return Response({
            "status": "Sync déclenché",
            "package_id": package.id
        })
