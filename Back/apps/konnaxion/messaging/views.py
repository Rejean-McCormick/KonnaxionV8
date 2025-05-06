from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from konnaxion.messaging.models import Conversation, Message
from konnaxion.messaging.serializers import ConversationSerializer, MessageSerializer
# Exemple : Importer une tâche pour notifier en temps réel (WebSocket/Celery)
# from konnaxion.messaging.tasks import notify_new_message

class ConversationViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des conversations.
    """
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les conversations auxquelles participe l'utilisateur
        return Conversation.objects.filter(participants=self.request.user)

    def perform_create(self, serializer):
        # Crée la conversation et ajoute automatiquement l'utilisateur
        conversation = serializer.save()
        conversation.participants.add(self.request.user)


class MessageViewSet(viewsets.ModelViewSet):
    """
    Endpoints pour la gestion des messages.
    """
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ne renvoie que les messages dans les conversations de l'utilisateur
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement l'utilisateur comme expéditeur
        message = serializer.save(sender=self.request.user)
        # Exemple : notifier en temps réel
        # notify_new_message.delay(message.id)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_as_read(self, request, pk=None):
        """
        Action personnalisée pour marquer un message comme lu.
        """
        message = self.get_object()
        message.is_read = True
        message.save()
        return Response({"status": "Message marqué comme lu"})
