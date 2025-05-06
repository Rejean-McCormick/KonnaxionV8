# apps/konnaxion/ekoh/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from konnaxion.ekoh.models import ExpertiseTag, ReputationProfile, ReputationEvent, WeightedVote

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests des modèles (Model Tests)
# ------------------------------------------------------------------------------

class ExpertiseTagModelTests(TestCase):
    def test_create_expertise_tag(self):
        """
        Crée une expertise tag et vérifie que ses champs sont correctement enregistrés.
        La représentation en chaîne doit renvoyer le nom du tag.
        """
        tag = ExpertiseTag.objects.create(
            name="Python",
            description="Expertise en programmation Python"
        )
        self.assertEqual(tag.name, "Python")
        self.assertEqual(tag.description, "Expertise en programmation Python")
        self.assertEqual(str(tag), "Python")


class ReputationProfileModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="ekoh_user", password="ekohpass", email="ekoh_user@example.com"
        )
        self.tag1 = ExpertiseTag.objects.create(
            name="Django", description="Expertise sur le framework Django"
        )
        self.tag2 = ExpertiseTag.objects.create(
            name="REST", description="Expertise en conception d'API REST"
        )
        self.profile = ReputationProfile.objects.create(
            user=self.user, reputation_score=50.0, ethical_multiplier=1.2
        )
        self.profile.expertise_tags.add(self.tag1, self.tag2)
    
    def test_reputation_profile_tags(self):
        """
        Vérifie que le profil de réputation possède bien les tags d'expertise assignés.
        """
        self.assertEqual(self.profile.expertise_tags.count(), 2)
        tag_names = list(self.profile.expertise_tags.values_list('name', flat=True))
        self.assertIn("Django", tag_names)
        self.assertIn("REST", tag_names)
    
    def test_reputation_profile_str(self):
        """
        Vérifie que la représentation en chaîne du profil de réputation est conforme.
        On suppose qu'elle renvoie "Reputation Profile for <username>".
        """
        expected_str = f"Reputation Profile for {self.user.username}"
        self.assertEqual(str(self.profile), expected_str)


class ReputationEventModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="event_user", password="eventpass", email="event_user@example.com"
        )
        self.profile = ReputationProfile.objects.create(
            user=self.user, reputation_score=30.0, ethical_multiplier=1.0
        )
    
    def test_create_reputation_event(self):
        """
        Crée un événement de réputation et vérifie que ses valeurs (type, valeur, description) sont correctes.
        """
        event = ReputationEvent.objects.create(
            reputation_profile=self.profile,
            event_type="vote",
            event_value=5.0,
            description="Upvote sur un argument"
        )
        self.assertEqual(event.event_type, "vote")
        self.assertEqual(event.event_value, 5.0)
        self.assertEqual(event.description, "Upvote sur un argument")
        # On vérifie que la représentation en chaîne contient le nom d'utilisateur
        self.assertIn(self.user.username, str(event))


class WeightedVoteModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="vote_user", password="votepass", email="vote_user@example.com"
        )
    
    def test_create_weighted_vote(self):
        """
        Crée un vote pondéré et vérifie que les valeurs target_id, vote_value et weight sont enregistrées correctement.
        """
        vote = WeightedVote.objects.create(
            user=self.user,
            target_id=42,
            vote_value=1,
            weight=2.5
        )
        self.assertEqual(vote.user, self.user)
        self.assertEqual(vote.target_id, 42)
        self.assertEqual(vote.vote_value, 1)
        self.assertEqual(vote.weight, 2.5)
        self.assertIn("vote_user", str(vote))


# ------------------------------------------------------------------------------
# 2. Tests des endpoints API pour le module ekoh (API Tests)
# ------------------------------------------------------------------------------

class ReputationProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_ekoh", password="apipass", email="api_ekoh@example.com"
        )
        self.client.login(username="api_ekoh", password="apipass")
        self.profile = ReputationProfile.objects.create(
            user=self.user, reputation_score=75.0, ethical_multiplier=1.1
        )
    
    def test_list_reputation_profiles(self):
        """
        Vérifie que l'API retourne la liste des profils de réputation.
        On suppose que le basename dans le routeur DRF est "reputationprofile".
        """
        url = reverse("reputationprofile-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)


class WeightedVoteAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_vote", password="apipass", email="api_vote@example.com"
        )
        self.client.login(username="api_vote", password="apipass")
    
    def test_create_weighted_vote_via_api(self):
        """
        Teste la création d'un vote pondéré via l'API.
        On suppose que le basename configuré dans le routeur DRF est "weightedvote".
        """
        url = reverse("weightedvote-list")
        data = {
            "user": self.user.id,
            "target_id": 100,
            "vote_value": -1,
            "weight": 3.0
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(WeightedVote.objects.count(), 1)
        vote = WeightedVote.objects.first()
        self.assertEqual(vote.vote_value, -1)
        self.assertEqual(vote.weight, 3.0)


class ExpertiseTagAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_tag", password="apipass", email="api_tag@example.com"
        )
        self.client.login(username="api_tag", password="apipass")
        ExpertiseTag.objects.create(name="API Tag 1", description="Premier tag API")
        ExpertiseTag.objects.create(name="API Tag 2", description="Deuxième tag API")
    
    def test_list_expertise_tags(self):
        """
        Vérifie que l'API retourne la liste des tags d'expertise.
        On suppose que le basename dans le routeur DRF est "expertisetag".
        """
        url = reverse("expertisetag-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)


class ReputationEventAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_event", password="apipass", email="api_event@example.com"
        )
        self.client.login(username="api_event", password="apipass")
        self.profile = ReputationProfile.objects.create(
            user=self.user, reputation_score=60.0, ethical_multiplier=1.0
        )
        ReputationEvent.objects.create(
            reputation_profile=self.profile,
            event_type="contribution",
            event_value=10.0,
            description="Contribution à un débat"
        )
    
    def test_list_reputation_events(self):
        """
        Vérifie que l'API retourne la liste des événements de réputation.
        On suppose que le basename dans le routeur DRF est "reputationevent".
        """
        url = reverse("reputationevent-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
