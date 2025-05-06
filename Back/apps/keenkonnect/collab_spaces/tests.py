# apps/keenkonnect/collab_spaces/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from keenkonnect.collab_spaces.models import CollabSpace, Document, ChatMessage

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class CollabSpaceModelTests(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="collab_user1", password="pass123", email="collab1@example.com")
        self.user2 = User.objects.create_user(username="collab_user2", password="pass123", email="collab2@example.com")
    
    def test_create_collab_space(self):
        """
        Crée un espace collaboratif, y ajoute des participants et vérifie la représentation en chaîne.
        """
        space = CollabSpace.objects.create(
            name="Espace Collaboratif Test",
            description="Espace pour tests unitaires."
        )
        space.participants.add(self.user1, self.user2)
        self.assertEqual(space.name, "Espace Collaboratif Test")
        self.assertEqual(space.participants.count(), 2)
        # On vérifie que la représentation en chaîne contient les noms d'utilisateur
        space_str = str(space)
        self.assertIn(self.user1.username, space_str)
        self.assertIn(self.user2.username, space_str)


class DocumentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="doc_user", password="pass123", email="doc_user@example.com")
        self.space = CollabSpace.objects.create(
            name="Espace pour Documents",
            description="Test de documents dans l'espace collaboratif."
        )
        self.space.participants.add(self.user)
    
    def test_create_document(self):
        """
        Crée un document associé à un espace collaboratif et vérifie ses champs.
        Pour le champ 'file', nous utilisons un chemin fictif pour le test.
        """
        document = Document.objects.create(
            collab_space=self.space,
            title="Document Test",
            file="collab_documents/test_file.pdf",
            description="Document de test",
            uploaded_by=self.user
        )
        self.assertEqual(document.title, "Document Test")
        self.assertEqual(document.file, "collab_documents/test_file.pdf")
        self.assertEqual(document.description, "Document de test")
        self.assertEqual(document.uploaded_by, self.user)


class ChatMessageModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="chat_user", password="pass123", email="chat_user@example.com")
        self.space = CollabSpace.objects.create(
            name="Espace Chat",
            description="Test de chat dans l'espace collaboratif."
        )
        self.space.participants.add(self.user)
    
    def test_create_chat_message(self):
        """
        Crée un message dans un espace collaboratif et vérifie que le contenu, l'expéditeur et la représentation en chaîne sont corrects.
        """
        message = ChatMessage.objects.create(
            collab_space=self.space,
            sender=self.user,
            message="Bonjour, ceci est un message test."
        )
        self.assertEqual(message.sender, self.user)
        self.assertEqual(message.collab_space, self.space)
        self.assertEqual(message.message, "Bonjour, ceci est un message test.")
        self.assertIn("Message from", str(message))
        

# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class CollabSpaceAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié et un espace collaboratif initial pour les tests API.
        """
        self.user1 = User.objects.create_user(username="api_collab1", password="apipass", email="api_collab1@example.com")
        self.user2 = User.objects.create_user(username="api_collab2", password="apipass", email="api_collab2@example.com")
        self.client.login(username="api_collab1", password="apipass")
        self.space = CollabSpace.objects.create(
            name="API Collab Space",
            description="Espace collaboratif créé via l'API."
        )
        self.space.participants.add(self.user1)
    
    def test_list_collab_spaces(self):
        """
        Vérifie que l'API retourne la liste des espaces collaboratifs auxquels l'utilisateur authentifié participe.
        On suppose que le basename dans le routeur DRF est "collabspace".
        """
        url = reverse("collabspace-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_add_participant_action(self):
        """
        Vérifie l'action personnalisée 'add_participant' qui permet d'ajouter un participant à un espace collaboratif.
        On suppose que le ViewSet expose cette action via l'URL nommée "collabspace-add-participant".
        """
        url = reverse("collabspace-add-participant", kwargs={"pk": self.space.pk})
        data = {"user_id": self.user2.id}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.space.refresh_from_db()
        self.assertEqual(self.space.participants.count(), 2)
        self.assertIn(self.user2.id, self.space.participants.values_list("id", flat=True))


class DocumentAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié et un espace collaboratif, puis crée un document initial pour tester l'API.
        """
        self.user = User.objects.create_user(username="api_doc", password="apipass", email="api_doc@example.com")
        self.client.login(username="api_doc", password="apipass")
        self.space = CollabSpace.objects.create(
            name="API Collab Space for Documents",
            description="Espace pour tester la gestion des documents."
        )
        self.space.participants.add(self.user)
        self.document = Document.objects.create(
            collab_space=self.space,
            title="API Document",
            file="collab_documents/api_file.pdf",
            description="Document créé via l'API.",
            uploaded_by=self.user
        )
    
    def test_list_documents(self):
        """
        Vérifie que l'API retourne la liste des documents pour un espace collaboratif.
        On suppose que le basename dans le routeur DRF est "document".
        """
        url = reverse("document-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_document_api(self):
        """
        Vérifie la création d'un document via l'API.
        """
        url = reverse("document-list")
        data = {
            "collab_space": self.space.id,
            "title": "New API Document",
            "file": "collab_documents/new_api_file.pdf",
            "description": "Nouveau document créé via l'API.",
            "uploaded_by": self.user.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Document.objects.filter(title="New API Document").count(), 1)


class ChatMessageAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié et un espace collaboratif pour tester l'API des messages de chat.
        """
        self.user = User.objects.create_user(username="api_chat", password="apipass", email="api_chat@example.com")
        self.client.login(username="api_chat", password="apipass")
        self.space = CollabSpace.objects.create(
            name="API Collab Space for Chat",
            description="Espace collaboratif pour tester le chat."
        )
        self.space.participants.add(self.user)
        self.message = ChatMessage.objects.create(
            collab_space=self.space,
            sender=self.user,
            message="Message initial via l'API"
        )
    
    def test_list_chat_messages(self):
        """
        Vérifie que l'API retourne la liste des messages de chat pour un espace collaboratif.
        On suppose que le basename dans le routeur DRF est "chatmessage".
        """
        url = reverse("chatmessage-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_chat_message_api(self):
        """
        Vérifie que l'on peut créer un nouveau message de chat via l'API.
        """
        url = reverse("chatmessage-list")
        data = {
            "collab_space": self.space.id,
            "sender": self.user.id,
            "message": "Nouveau message via l'API"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ChatMessage.objects.filter(message="Nouveau message via l'API").count(), 1)
    
    def test_mark_chat_message_as_read(self):
        """
        Vérifie l'action personnalisée 'mark_as_read' pour marquer un message de chat comme lu.
        On suppose que le ViewSet expose cette action via l'URL nommée "chatmessage-mark-as-read".
        """
        url = reverse("chatmessage-mark-as-read", kwargs={"pk": self.message.pk})
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.message.refresh_from_db()
        # Supposons que l'action modifie un champ 'is_read' dans le modèle ChatMessage
        self.assertTrue(getattr(self.message, "is_read", True))
