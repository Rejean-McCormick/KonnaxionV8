# apps/keenkonnect/team_formation/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

# Importer les modèles du module team_formation
from keenkonnect.team_formation.models import TeamFormationRequest, TeamFormationCandidate
# On suppose que TeamFormationRequest est lié à un projet du module projects
from keenkonnect.projects.models import Project

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class TeamFormationRequestModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="team_former", password="pass123", email="team_former@example.com"
        )
        self.project = Project.objects.create(
            title="Project for Team Formation",
            description="Projet de test pour formation d'équipe.",
            owner=self.user,
            progress=0,
            status="planning"
        )

    def test_create_team_formation_request(self):
        """
        Teste la création d'une instance de TeamFormationRequest.
        Vérifie que les champs 'project', 'requested_by', 'required_roles' et 'additional_info'
        sont correctement enregistrés et que la représentation en chaîne contient le titre du projet.
        """
        request_obj = TeamFormationRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            required_roles={"role": "developer"},
            additional_info="Besoin d'une équipe pour le développement backend."
        )
        self.assertEqual(request_obj.project, self.project)
        self.assertEqual(request_obj.requested_by, self.user)
        self.assertEqual(request_obj.required_roles, {"role": "developer"})
        self.assertEqual(request_obj.additional_info, "Besoin d'une équipe pour le développement backend.")
        self.assertIn(self.project.title, str(request_obj))


class TeamFormationCandidateModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="team_candidate", password="pass123", email="team_candidate@example.com"
        )
        self.project = Project.objects.create(
            title="Project for Candidate Testing",
            description="Projet pour tester les candidats en formation d'équipe.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.request_obj = TeamFormationRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            required_roles={"role": "designer"},
            additional_info="Recherche d'un designer créatif."
        )

    def test_create_team_formation_candidate(self):
        """
        Teste la création d'une instance de TeamFormationCandidate.
        Vérifie que 'formation_request', 'user', 'skills' et 'compatibility_score' sont correctement enregistrés.
        """
        candidate = TeamFormationCandidate.objects.create(
            formation_request=self.request_obj,
            user=self.user,
            skills={"design": "Photoshop"},
            compatibility_score=75.0
        )
        self.assertEqual(candidate.formation_request, self.request_obj)
        self.assertEqual(candidate.user, self.user)
        self.assertEqual(candidate.skills, {"design": "Photoshop"})
        self.assertEqual(candidate.compatibility_score, 75.0)
        self.assertIn(self.user.username, str(candidate))


# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class TeamFormationRequestAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié, un projet et une demande de formation d'équipe initiale
        pour tester les endpoints API du module team_formation.
        """
        self.user = User.objects.create_user(
            username="api_team_former", password="apipass", email="api_team_former@example.com"
        )
        self.client.login(username="api_team_former", password="apipass")
        self.project = Project.objects.create(
            title="API Project for Team Formation",
            description="Projet API pour tester la formation d'équipe.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.request_obj = TeamFormationRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            required_roles={"role": "tester"},
            additional_info="Besoin d'une équipe pour tester le projet."
        )

    def test_list_team_formation_requests(self):
        """
        Vérifie que l'API retourne la liste des TeamFormationRequest.
        On suppose que le basename dans le routeur DRF est "teamformationrequest".
        """
        url = reverse("teamformationrequest-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_team_formation_request_api(self):
        """
        Vérifie la création d'une nouvelle TeamFormationRequest via l'API.
        """
        url = reverse("teamformationrequest-list")
        data = {
            "project": self.project.id,
            "requested_by": self.user.id,
            "required_roles": {"role": "analyst"},
            "additional_info": "Recherche d'un analyste pour le projet."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamFormationRequest.objects.filter(additional_info="Recherche d'un analyste pour le projet.").count(), 1)


class TeamFormationCandidateAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié, un projet et une demande de formation d'équipe,
        puis crée un candidat initial pour tester les endpoints du module team_formation.
        """
        self.user = User.objects.create_user(
            username="api_team_candidate", password="apipass", email="api_team_candidate@example.com"
        )
        self.client.login(username="api_team_candidate", password="apipass")
        self.project = Project.objects.create(
            title="API Project for Candidate Testing",
            description="Projet pour tester l'API des candidats en formation d'équipe.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.request_obj = TeamFormationRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            required_roles={"role": "engineer"},
            additional_info="Besoin d'un ingénieur backend."
        )
        self.candidate_obj = TeamFormationCandidate.objects.create(
            formation_request=self.request_obj,
            user=self.user,
            skills={"backend": "Python"},
            compatibility_score=80.0
        )

    def test_list_team_formation_candidates(self):
        """
        Vérifie que l'API retourne la liste des TeamFormationCandidate.
        On suppose que le basename dans le routeur DRF est "teamformationcandidate".
        """
        url = reverse("teamformationcandidate-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_team_formation_candidate_api(self):
        """
        Vérifie la création d'une nouvelle TeamFormationCandidate via l'API.
        """
        url = reverse("teamformationcandidate-list")
        data = {
            "formation_request": self.request_obj.id,
            "user": self.user.id,
            "skills": {"backend": "Django"},
            "compatibility_score": 85.0
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamFormationCandidate.objects.filter(compatibility_score=85.0).count(), 1)
