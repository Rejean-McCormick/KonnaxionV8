# apps/konnaxion/notifications/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from konnaxion.notifications.models import Notification

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests du modèle Notification
# ------------------------------------------------------------------------------

class NotificationModelTests(TestCase):
    def test_create_notification(self):
        """
        Teste la création d'une notification et sa représentation en chaîne.
        - Vérifie que le message et le type sont correctement enregistrés.
        - Vérifie que la notification est initialement non lue.
        """
        sender = User.objects.create_user(
            username="expediteur", password="pass123", email="expediteur@example.com"
        )
        recipient = User.objects.create_user(
            username="destinataire", password="pass456", email="destinataire@example.com"
        )
        notification = Notification.objects.create(
            sender=sender,
            recipient=recipient,
            message="Ceci est un test de notification.",
            notification_type="info"
        )
        self.assertEqual(notification.message, "Ceci est un test de notification.")
        self.assertEqual(notification.notification_type, "info")
        self.assertFalse(notification.is_read)
        # Vérifie la représentation en chaîne (selon le __str__ défini dans le modèle)
        expected_str = f"Notification for {recipient} - Info"
        self.assertEqual(str(notification), expected_str)


# ------------------------------------------------------------------------------
# 2. Tests des endpoints API pour Notification
# ------------------------------------------------------------------------------

class NotificationAPITests(APITestCase):
    def setUp(self):
        """
        Crée des utilisateurs et une notification de test, puis authentifie l'utilisateur destinataire.
        """
        self.sender = User.objects.create_user(
            username="api_expediteur", password="apipass", email="api_expediteur@example.com"
        )
        self.recipient = User.objects.create_user(
            username="api_destinataire", password="apipass", email="api_destinataire@example.com"
        )
        # Authentification en tant que destinataire (celui qui reçoit les notifications)
        self.client.login(username="api_destinataire", password="apipass")
        self.notification = Notification.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            message="Notification API test",
            notification_type="warning"
        )
    
    def test_list_notifications(self):
        """
        Vérifie que l'API renvoie la liste des notifications pour l'utilisateur authentifié.
        On suppose que le basename utilisé dans le routeur DRF est "notification".
        """
        url = reverse("notification-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # On s'assure qu'au moins la notification de test est présente dans la réponse
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_mark_notification_as_read(self):
        """
        Vérifie que l'action personnalisée 'mark_as_read' permet de marquer une notification comme lue.
        On suppose que le ViewSet expose une action 'mark_as_read' accessible via une URL nommée "notification-mark-as-read".
        """
        url = reverse("notification-mark-as-read", kwargs={"pk": self.notification.pk})
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Recharge l'instance depuis la base de données et vérifie que le champ is_read est désormais True
        self.notification.refresh_from_db()
        self.assertTrue(self.notification.is_read)
