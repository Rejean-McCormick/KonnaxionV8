from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from konnaxion.notifications.models import Notification
from konnaxion.notifications.serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les notifications du destinataire connecté
        return Notification.objects.filter(recipient=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        """
        Marquer une notification comme lue.
        """
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({"status": "Notification marquée comme lue"})

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def unread(self, request):
        """
        Retourne la liste des notifications non lues pour l'utilisateur connecté.
        """
        qs = self.get_queryset().filter(is_read=False)
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
