# apps/konnected/paths/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from konnected.paths.models import LearningPath, PathStep
from konnected.foundation.models import KnowledgeUnit

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class LearningPathModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="path_creator", password="pass123", email="path_creator@example.com"
        )
    
    def test_create_learning_path(self):
        """
        Teste la création d'une instance de LearningPath.
        Vérifie que le titre, la description et le créateur sont correctement enregistrés,
        et que la représentation en chaîne retourne le titre.
        """
        path = LearningPath.objects.create(
            title="Curriculum Python",
            description="Un parcours pour apprendre le développement en Python.",
            created_by=self.user
        )
        self.assertEqual(path.title, "Curriculum Python")
        self.assertEqual(path.description, "Un parcours pour apprendre le développement en Python.")
        self.assertEqual(path.created_by, self.user)
        # Supposons que la méthode __str__ retourne simplement le titre.
        self.assertEqual(str(path), "Curriculum Python")


class PathStepModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="step_creator", password="pass123", email="step_creator@example.com"
        )
        self.learning_path = LearningPath.objects.create(
            title="Data Science Path",
            description="Parcours pour apprendre la data science.",
            created_by=self.user
        )
        # Création d'une instance de KnowledgeUnit (modèle défini dans l'app foundation)
        self.knowledge_unit = KnowledgeUnit.objects.create(
            title="Introduction aux statistiques",
            content="Notions de base en statistiques.",
            attachments=[]  # On peut utiliser une liste vide
        )
    
    def test_create_path_step(self):
        """
        Teste la création d'une instance de PathStep.
        Vérifie que l'étape est bien associée au parcours et à la knowledge unit, et que l'ordre est correct.
        La représentation en chaîne doit être du type :
        "<LearningPath.title> - Step <order>: <KnowledgeUnit.title>"
        """
        step = PathStep.objects.create(
            learning_path=self.learning_path,
            knowledge_unit=self.knowledge_unit,
            order=1
        )
        self.assertEqual(step.learning_path, self.learning_path)
        self.assertEqual(step.knowledge_unit, self.knowledge_unit)
        self.assertEqual(step.order, 1)
        expected_str = f"{self.learning_path.title} - Step 1: {self.knowledge_unit.title}"
        self.assertEqual(str(step), expected_str)


# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class LearningPathAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur pour l'authentification et une instance initiale de LearningPath.
        """
        self.user = User.objects.create_user(
            username="api_path_creator", password="apipass", email="api_path_creator@example.com"
        )
        self.client.login(username="api_path_creator", password="apipass")
        self.learning_path = LearningPath.objects.create(
            title="API Learning Path",
            description="Parcours créé via l'API.",
            created_by=self.user
        )
    
    def test_list_learning_paths(self):
        """
        Vérifie que l'API retourne la liste des LearningPath.
        On suppose que le basename configuré dans le routeur DRF est "learningpath".
        """
        url = reverse("learningpath-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_learning_path_api(self):
        """
        Vérifie que l'on peut créer une nouvelle instance de LearningPath via l'API.
        """
        url = reverse("learningpath-list")
        data = {
            "title": "New API Learning Path",
            "description": "Ce parcours est créé via l'API.",
            "created_by": self.user.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LearningPath.objects.filter(title="New API Learning Path").count(), 1)


class PathStepAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur authentifié, crée une instance de LearningPath et une KnowledgeUnit,
        puis crée une première étape (PathStep) pour le parcours.
        """
        self.user = User.objects.create_user(
            username="api_step_creator", password="apipass", email="api_step_creator@example.com"
        )
        self.client.login(username="api_step_creator", password="apipass")
        self.learning_path = LearningPath.objects.create(
            title="API Data Science Path",
            description="Parcours API pour la data science.",
            created_by=self.user
        )
        self.knowledge_unit = KnowledgeUnit.objects.create(
            title="API: Introduction à l'apprentissage automatique",
            content="Notions de base sur le machine learning.",
            attachments=[]
        )
        self.path_step = PathStep.objects.create(
            learning_path=self.learning_path,
            knowledge_unit=self.knowledge_unit,
            order=1
        )
    
    def test_list_path_steps(self):
        """
        Vérifie que l'API retourne la liste des PathStep pour un LearningPath donné.
        On suppose que l'URL est configurée de façon imbriquée, par exemple :
        /api/learning_paths/<learning_path_pk>/path_steps/ avec le basename "pathstep".
        """
        url = reverse("pathstep-list", kwargs={"learning_path_pk": self.learning_path.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_path_step_api(self):
        """
        Vérifie que l'on peut créer une nouvelle PathStep via l'API pour un LearningPath donné.
        """
        url = reverse("pathstep-list", kwargs={"learning_path_pk": self.learning_path.pk})
        data = {
            "knowledge_unit": self.knowledge_unit.id,
            "order": 2
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PathStep.objects.filter(learning_path=self.learning_path, order=2).count(), 1)
