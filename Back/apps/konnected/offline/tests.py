# apps/konnected/offline/tests.py

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from konnected.offline.models import OfflineContentPackage

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class OfflineContentPackageModelTests(TestCase):
    def test_create_offline_content_package(self):
        """
        Teste la création d'un OfflineContentPackage.
        Vérifie que les champs title, description, content_data et conflict_resolution_notes
        sont correctement enregistrés, et que les champs d'audit (created_at, updated_at) sont renseignés.
        """
        package = OfflineContentPackage.objects.create(
            title="Package Offline Test",
            description="Description du package test",
            content_data={"modules": ["module1", "module2"]},
            conflict_resolution_notes="Aucun conflit détecté"
        )
        self.assertEqual(package.title, "Package Offline Test")
        self.assertEqual(package.description, "Description du package test")
        self.assertEqual(package.content_data, {"modules": ["module1", "module2"]})
        self.assertEqual(package.conflict_resolution_notes, "Aucun conflit détecté")
        # Vérifie que created_at et updated_at sont renseignés
        self.assertIsNotNone(package.created_at)
        self.assertIsNotNone(package.updated_at)


# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class OfflineContentPackageAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié et une instance initiale de OfflineContentPackage
        pour tester les endpoints API.
        """
        self.user = User.objects.create_user(
            username="offline_api", password="apipass", email="offline_api@example.com"
        )
        self.client.login(username="offline_api", password="apipass")
        self.package = OfflineContentPackage.objects.create(
            title="API Offline Package",
            description="Package créé via l'API",
            content_data={"files": ["file1", "file2"]},
            conflict_resolution_notes=""
        )

    def test_list_offline_packages(self):
        """
        Vérifie que l'API retourne la liste des OfflineContentPackage.
        On suppose que le basename configuré dans le routeur DRF est "offline_packages".
        """
        url = reverse("offline_packages-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Au moins l'instance créée dans setUp doit être présente
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_offline_package_api(self):
        """
        Vérifie que l'on peut créer une nouvelle instance d'OfflineContentPackage via l'API.
        """
        url = reverse("offline_packages-list")
        data = {
            "title": "New API Offline Package",
            "description": "Contenu du package créé via l'API",
            "content_data": {"files": ["new_file1", "new_file2"]},
            "conflict_resolution_notes": "Test"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(OfflineContentPackage.objects.filter(title="New API Offline Package").count(), 1)

    def test_sync_offline_package_action(self):
        """
        Vérifie l'action personnalisée 'sync' qui déclenche la synchronisation d'un OfflineContentPackage.
        On suppose que le ViewSet expose une action 'sync' accessible via l'URL nommée "offline_packages-sync".
        Après l'appel, le champ last_synced doit être mis à jour.
        """
        url = reverse("offline_packages-sync", kwargs={"pk": self.package.pk})
        data = {}  # Données éventuelles à passer, si nécessaire
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Recharge l'instance depuis la base de données et vérifie que last_synced a été mis à jour
        self.package.refresh_from_db()
        self.assertIsNotNone(self.package.last_synced)
        # Vérifie que la valeur de last_synced est proche de l'heure actuelle (delta de 5 secondes)
        self.assertAlmostEqual(
            self.package.last_synced.timestamp(),
            timezone.now().timestamp(),
            delta=5
        )
