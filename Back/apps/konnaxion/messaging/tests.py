# apps/konnaxion/messaging/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from konnaxion.messaging.models import Conversation, Message

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests des modèles (Model Tests)
# ------------------------------------------------------------------------------

class ConversationModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="mess1", password="pass1", email="mess1@example.com")
        self.user2 = User.objects.create_user(username="mess2", password="pass2", email="mess2@example.com")
    
    def test_create_conversation(self):
        """
        Crée une conversation avec un titre et y ajoute deux participants.
        Vérifie que le titre et le nombre de participants sont corrects,
        ainsi que le comportement de la méthode __str__.
        """
        conversation = Conversation.objects.create(title="Conversation de Test")
        conversation.participants.add(self.user1, self.user2)
        self.assertEqual(conversation.title, "Conversation de Test")
        self.assertEqual(conversation.participants.count(), 2)
        # Vérifie que le __str__ inclut les usernames des participants
        conv_str = str(conversation)
        self.assertIn(self.user1.username, conv_str)
        self.assertIn(self.user2.username, conv_str)


class MessageModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="mess3", password="pass3", email="mess3@example.com")
        self.user2 = User.objects.create_user(username="mess4", password="pass4", email="mess4@example.com")
        self.conversation = Conversation.objects.create(title="Conversation pour Messages")
        self.conversation.participants.add(self.user1, self.user2)
    
    def test_create_message(self):
        """
        Crée un message dans une conversation et vérifie que le contenu,
        l'expéditeur et le statut de lecture (is_read) sont correctement enregistrés.
        """
        message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Ceci est un message de test."
        )
        self.assertEqual(message.content, "Ceci est un message de test.")
        self.assertFalse(message.is_read)
        self.assertEqual(message.sender, self.user1)
        self.assertEqual(message.conversation, self.conversation)
        # Vérifie la représentation en chaîne
        self.assertIn("Message from", str(message))

# ------------------------------------------------------------------------------
# 2. Tests des endpoints API (API Tests)
# ------------------------------------------------------------------------------

class MessagingAPITests(APITestCase):
    def setUp(self):
        """
        Prépare les données de test en créant deux utilisateurs et en
        initialisant une conversation et un message.
        L'utilisateur authentifié sera le premier utilisateur.
        """
        self.user1 = User.objects.create_user(username="api_mess1", password="apipass", email="api_mess1@example.com")
        self.user2 = User.objects.create_user(username="api_mess2", password="apipass", email="api_mess2@example.com")
        self.client.login(username="api_mess1", password="apipass")
        self.conversation = Conversation.objects.create(title="Conversation API Test")
        self.conversation.participants.add(self.user1, self.user2)
        self.message = Message.objects.create(
            conversation=self.conversation,
            sender=self.user1,
            content="Message envoyé via l'API."
        )

    def test_list_conversations(self):
        """
        Vérifie que l'API retourne la liste des conversations auxquelles l'utilisateur authentifié participe.
        On suppose que le basename dans le routeur DRF est "conversation".
        """
        url = reverse("conversation-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # On s'attend à trouver au moins une conversation
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_messages_in_conversation(self):
        """
        Vérifie que l'API retourne la liste des messages pour une conversation donnée.
        On suppose que l'URL est définie par un routeur imbriqué (par exemple, avec le basename "conversation-messages").
        """
        # L'URL doit inclure l'identifiant de la conversation, par exemple :
        url = reverse("conversation-messages", kwargs={"conversation_pk": self.conversation.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # On s'attend à au moins trouver le message créé dans setUp
        self.assertGreaterEqual(len(response.data), 1)

    def test_mark_message_as_read(self):
        """
        Vérifie que l'action personnalisée pour marquer un message comme lu fonctionne.
        On suppose que le ViewSet pour Message expose une action 'mark_as_read'
        accessible via l'URL nommée "message-mark-as-read".
        """
        url = reverse("message-mark-as-read", kwargs={"pk": self.message.pk})
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        self.assertTrue(self.message.is_read)
