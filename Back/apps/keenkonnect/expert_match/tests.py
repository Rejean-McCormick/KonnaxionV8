# apps/keenkonnect/expert_match/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

# Importation des modèles du module expert_match
from keenkonnect.expert_match.models import ExpertMatchRequest, CandidateProfile, MatchScore
# Importation du modèle Project pour l'association (issu du module projects)
from keenkonnect.projects.models import Project

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class ExpertMatchRequestModelTests(TestCase):
    def setUp(self):
        # Crée un utilisateur et un projet pour la demande d'expert
        self.user = User.objects.create_user(
            username="expert_user", password="pass", email="expert_user@example.com"
        )
        self.project = Project.objects.create(
            title="Projet Expert",
            description="Projet pour tester la demande de matching expert.",
            owner=self.user,
            progress=0,
            status="planning"
        )

    def test_create_expert_match_request(self):
        """
        Teste la création d'une instance d'ExpertMatchRequest.
        Vérifie que les champs 'project', 'requested_by', 'description' et 'criteria'
        sont correctement enregistrés.
        """
        request = ExpertMatchRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            description="Besoin d'un expert pour améliorer le projet.",
            criteria={"experience": "5+ ans", "skills": ["Django", "REST"]}
        )
        self.assertEqual(request.project, self.project)
        self.assertEqual(request.requested_by, self.user)
        self.assertEqual(request.description, "Besoin d'un expert pour améliorer le projet.")
        self.assertEqual(request.criteria, {"experience": "5+ ans", "skills": ["Django", "REST"]})
        # Vérifie que la représentation en chaîne inclut le titre du projet
        self.assertIn(self.project.title, str(request))


class CandidateProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="candidate_user", password="pass", email="candidate_user@example.com"
        )
    
    def test_create_candidate_profile(self):
        """
        Teste la création d'un CandidateProfile.
        Vérifie que les champs 'user', 'skills' et 'reputation_score' sont correctement enregistrés.
        """
        profile = CandidateProfile.objects.create(
            user=self.user,
            skills={"languages": ["Python", "JavaScript"]},
            reputation_score=85.5
        )
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.skills, {"languages": ["Python", "JavaScript"]})
        self.assertEqual(profile.reputation_score, 85.5)
        self.assertIn(self.user.username, str(profile))


class MatchScoreModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="match_user", password="pass", email="match_user@example.com"
        )
        self.project = Project.objects.create(
            title="Projet pour MatchScore",
            description="Projet pour tester le score de correspondance.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.match_request = ExpertMatchRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            description="Demande de matching d'experts.",
            criteria={"field": "tech"}
        )
        self.candidate = CandidateProfile.objects.create(
            user=self.user,
            skills={"frameworks": ["Django"]},
            reputation_score=90.0
        )
    
    def test_create_match_score(self):
        """
        Teste la création d'une instance de MatchScore.
        Vérifie que 'match_request', 'candidate' et 'score' sont correctement enregistrés.
        """
        match_score = MatchScore.objects.create(
            match_request=self.match_request,
            candidate=self.candidate,
            score=95.0
        )
        self.assertEqual(match_score.match_request, self.match_request)
        self.assertEqual(match_score.candidate, self.candidate)
        self.assertEqual(match_score.score, 95.0)
        self.assertIn("95", str(match_score))


# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class ExpertMatchRequestAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur authentifié, crée un projet et une demande d'expert initiale
        pour tester les endpoints API.
        """
        self.user = User.objects.create_user(
            username="api_expert", password="apipass", email="api_expert@example.com"
        )
        self.client.login(username="api_expert", password="apipass")
        self.project = Project.objects.create(
            title="API Project Expert",
            description="Projet API pour expert match request.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.expert_request = ExpertMatchRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            description="Besoin d'experts en API.",
            criteria={"experience": "3+ ans", "tools": ["DRF"]}
        )
    
    def test_list_expert_match_requests(self):
        """
        Vérifie que l'API retourne la liste des ExpertMatchRequest.
        On suppose que le basename dans le routeur DRF est "expertmatchrequest".
        """
        url = reverse("expertmatchrequest-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_expert_match_request_api(self):
        """
        Vérifie la création d'un ExpertMatchRequest via l'API.
        """
        url = reverse("expertmatchrequest-list")
        data = {
            "project": self.project.id,
            "requested_by": self.user.id,
            "description": "Nouvelle demande d'expert via API",
            "criteria": {"experience": "2+ ans", "skills": ["Python"]}
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ExpertMatchRequest.objects.filter(description="Nouvelle demande d'expert via API").count(), 1)


class CandidateProfileAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur authentifié et crée un CandidateProfile initial pour tester l'API.
        """
        self.user = User.objects.create_user(
            username="api_candidate", password="apipass", email="api_candidate@example.com"
        )
        self.client.login(username="api_candidate", password="apipass")
        self.candidate = CandidateProfile.objects.create(
            user=self.user,
            skills={"languages": ["Python", "JavaScript"]},
            reputation_score=88.0
        )
    
    def test_list_candidate_profiles(self):
        """
        Vérifie que l'API retourne la liste des CandidateProfile.
        On suppose que le basename dans le routeur DRF est "candidateprofile".
        """
        url = reverse("candidateprofile-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_candidate_profile_api(self):
        """
        Vérifie la création d'un CandidateProfile via l'API.
        """
        url = reverse("candidateprofile-list")
        data = {
            "user": self.user.id,
            "skills": {"frameworks": ["Django", "Flask"]},
            "reputation_score": 92.0
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CandidateProfile.objects.filter(reputation_score=92.0).count(), 1)


class MatchScoreAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur authentifié, crée un projet, une demande d'expert et un CandidateProfile,
        pour tester les endpoints du modèle MatchScore.
        """
        self.user = User.objects.create_user(
            username="api_match", password="apipass", email="api_match@example.com"
        )
        self.client.login(username="api_match", password="apipass")
        self.project = Project.objects.create(
            title="API Project for MatchScore",
            description="Projet pour tester MatchScore via API.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.expert_request = ExpertMatchRequest.objects.create(
            project=self.project,
            requested_by=self.user,
            description="Demande API pour expert matching.",
            criteria={"role": "backend"}
        )
        self.candidate = CandidateProfile.objects.create(
            user=self.user,
            skills={"frameworks": ["Django"]},
            reputation_score=85.0
        )
    
    def test_list_match_scores(self):
        """
        Vérifie que l'API retourne la liste des MatchScore.
        On suppose que le basename dans le routeur DRF est "matchscore".
        """
        url = reverse("matchscore-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Même s'il n'y a aucun score initial, on s'assure que la réponse est une liste
        self.assertIsInstance(response.data, list)
    
    def test_create_match_score_api(self):
        """
        Vérifie la création d'un MatchScore via l'API.
        """
        url = reverse("matchscore-list")
        data = {
            "match_request": self.expert_request.id,
            "candidate": self.candidate.id,
            "score": 93.0
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MatchScore.objects.filter(score=93.0).count(), 1)
