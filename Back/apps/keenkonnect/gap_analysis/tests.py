# apps/keenkonnect/gap_analysis/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

# Importation du modèle GapAnalysis depuis le module gap_analysis
from keenkonnect.gap_analysis.models import GapAnalysis
# Importation du modèle Project depuis le module projects (nécessaire pour l'association)
from keenkonnect.projects.models import Project

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class GapAnalysisModelTests(TestCase):
    def setUp(self):
        # Crée un utilisateur et un projet pour les tests de GapAnalysis
        self.user = User.objects.create_user(
            username="gap_user", password="pass123", email="gap_user@example.com"
        )
        self.project = Project.objects.create(
            title="Project for Gap Analysis",
            description="Projet de test pour l'analyse d'écart.",
            owner=self.user,
            progress=50,
            status="in_progress"
        )

    def test_create_gap_analysis(self):
        """
        Teste la création d'une instance de GapAnalysis.
        Vérifie que les valeurs de planned_progress, actual_progress, gap et recommendations
        sont correctement enregistrées et associées au projet.
        """
        gap = GapAnalysis.objects.create(
            project=self.project,
            planned_progress=80,
            actual_progress=50,
            gap=30,  # On peut aussi envisager de calculer cette valeur automatiquement.
            recommendations="Augmenter le suivi des jalons"
        )
        self.assertEqual(gap.project, self.project)
        self.assertEqual(gap.planned_progress, 80)
        self.assertEqual(gap.actual_progress, 50)
        self.assertEqual(gap.gap, 30)
        self.assertEqual(gap.recommendations, "Augmenter le suivi des jalons")
        # Vous pouvez ajouter ici un test sur la représentation en chaîne si __str__ est défini.


# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class GapAnalysisAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur authentifié, crée un projet et un enregistrement GapAnalysis initial.
        """
        self.user = User.objects.create_user(
            username="api_gap", password="apipass", email="api_gap@example.com"
        )
        self.client.login(username="api_gap", password="apipass")
        self.project = Project.objects.create(
            title="API Project for Gap Analysis",
            description="Projet API pour tester l'analyse d'écart.",
            owner=self.user,
            progress=40,
            status="in_progress"
        )
        self.gap_analysis = GapAnalysis.objects.create(
            project=self.project,
            planned_progress=70,
            actual_progress=40,
            gap=30,
            recommendations="Réviser la planification"
        )

    def test_list_gap_analyses(self):
        """
        Vérifie que l'API retourne la liste des enregistrements GapAnalysis.
        On suppose que le basename configuré dans le routeur DRF est "gap_analyses".
        """
        url = reverse("gap_analyses-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Au moins l'enregistrement créé dans setUp doit être présent.
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_gap_analysis_api(self):
        """
        Vérifie que l'on peut créer une nouvelle instance de GapAnalysis via l'API.
        """
        url = reverse("gap_analyses-list")
        data = {
            "project": self.project.id,
            "planned_progress": 90,
            "actual_progress": 60,
            "gap": 30,
            "recommendations": "Ajuster les délais et les ressources"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Vérifie que l'enregistrement est bien créé dans la base de données
        self.assertEqual(GapAnalysis.objects.filter(project=self.project, planned_progress=90).count(), 1)
