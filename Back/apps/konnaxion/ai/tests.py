# apps/konnaxion/ai/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from konnaxion.ai.models import AIResult

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests du modèle AIResult
# ------------------------------------------------------------------------------

class AIResultModelTests(TestCase):
    def test_create_ai_result(self):
        """
        Teste la création d'une instance d'AIResult.
        Vérifie que les champs result_type, result_data, source_model et source_object_id 
        sont correctement enregistrés.
        """
        ai_result = AIResult.objects.create(
            result_type="summary",
            result_data={"summary": "Ceci est un résumé de test."},
            source_model="Lesson",
            source_object_id=1
        )
        self.assertEqual(ai_result.result_type, "summary")
        self.assertEqual(ai_result.result_data, {"summary": "Ceci est un résumé de test."})
        self.assertEqual(ai_result.source_model, "Lesson")
        self.assertEqual(ai_result.source_object_id, 1)


# ------------------------------------------------------------------------------
# 2. Tests des endpoints API pour AIResult
# ------------------------------------------------------------------------------

class AIResultAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur de test, s'authentifie et crée une instance initiale d'AIResult
        pour les tests de l'API.
        """
        self.user = User.objects.create_user(
            username="aiuser",
            password="aipass",
            email="aiuser@example.com"
        )
        self.client.login(username="aiuser", password="aipass")
        self.ai_result = AIResult.objects.create(
            result_type="translation",
            result_data={"translated_text": "Bonjour"},
            source_model="Debate",
            source_object_id=2
        )
    
    def test_list_ai_results(self):
        """
        Vérifie que l'API retourne la liste des AIResult.
        """
        # On suppose que le basename configuré dans le routeur DRF est "airesult"
        url = reverse("airesult-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Vérifie que la liste contient au moins l'instance créée dans setUp
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_ai_result_via_api(self):
        """
        Teste la création d'une nouvelle instance d'AIResult via l'API.
        """
        url = reverse("airesult-list")
        data = {
            "result_type": "recommendation",
            "result_data": {"recommendation": "Utilisez cette approche pour optimiser la tâche."},
            "source_model": "Lesson",
            "source_object_id": 3
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que le nombre total d'instances est passé à 2
        self.assertEqual(AIResult.objects.count(), 2)
        new_result = AIResult.objects.get(source_object_id=3)
        self.assertEqual(new_result.result_type, "recommendation")
        self.assertEqual(new_result.result_data, {"recommendation": "Utilisez cette approche pour optimiser la tâche."})
