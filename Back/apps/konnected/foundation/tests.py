# apps/konnected/foundation/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from konnected.foundation.models import KnowledgeUnit

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests du modèle KnowledgeUnit
# ------------------------------------------------------------------------------

class KnowledgeUnitModelTests(TestCase):
    def test_create_knowledge_unit(self):
        """
        Teste la création d'une instance de KnowledgeUnit.
        Vérifie que les champs (title, content, attachments, language, version) sont correctement enregistrés,
        et que la méthode __str__ retourne le titre.
        """
        ku = KnowledgeUnit.objects.create(
            title="Test Knowledge Unit",
            content="Ceci est le contenu de test pour le knowledge unit.",
            attachments=["http://example.com/attachment1.png", "http://example.com/attachment2.png"]
        )
        self.assertEqual(ku.title, "Test Knowledge Unit")
        self.assertEqual(ku.content, "Ceci est le contenu de test pour le knowledge unit.")
        self.assertEqual(ku.attachments, ["http://example.com/attachment1.png", "http://example.com/attachment2.png"])
        # Les valeurs par défaut doivent être "en" pour language et 1 pour version.
        self.assertEqual(ku.language, "en")
        self.assertEqual(ku.version, 1)
        self.assertEqual(str(ku), "Test Knowledge Unit")

# ------------------------------------------------------------------------------
# 2. Tests des endpoints API pour KnowledgeUnit
# ------------------------------------------------------------------------------

class KnowledgeUnitAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur pour l'authentification et crée une instance de KnowledgeUnit
        pour tester les endpoints API.
        """
        self.user = User.objects.create_user(
            username="found_user", password="pass123", email="found_user@example.com"
        )
        self.client.login(username="found_user", password="pass123")
        self.ku = KnowledgeUnit.objects.create(
            title="API Knowledge Unit",
            content="Contenu généré pour le test API.",
            attachments=["http://example.com/api_attachment.png"]
        )

    def test_list_knowledge_units(self):
        """
        Vérifie que l'API retourne la liste des KnowledgeUnit.
        On suppose que l'endpoint est configuré via un routeur DRF avec le basename "knowledgeunit".
        """
        url = reverse("knowledgeunit-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # On s'attend à ce que la liste contienne au moins l'instance créée dans setUp
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_knowledge_unit_api(self):
        """
        Vérifie que l'on peut créer une nouvelle KnowledgeUnit via l'API.
        """
        url = reverse("knowledgeunit-list")
        data = {
            "title": "New API Knowledge Unit",
            "content": "Contenu créé via l'API.",
            "attachments": ["http://example.com/new_attachment.png"],
            "language": "fr",
            "version": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que le nombre total d'instances de KnowledgeUnit est passé à 2
        self.assertEqual(KnowledgeUnit.objects.count(), 2)
        new_ku = KnowledgeUnit.objects.get(title="New API Knowledge Unit")
        self.assertEqual(new_ku.content, "Contenu créé via l'API.")
        self.assertEqual(new_ku.language, "fr")
        self.assertEqual(new_ku.version, 2)
