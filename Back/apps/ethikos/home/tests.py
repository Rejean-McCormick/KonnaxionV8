# apps/ethikos/home/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from ethikos.home.models import DebateTopic, FeaturedDebate, PersonalizedRecommendation

User = get_user_model()

# --- Model Tests ---

class DebateTopicModelTests(TestCase):
    def test_create_debate_topic(self):
        topic = DebateTopic.objects.create(
            title="Test Debate Topic",
            description="Description of test debate topic.",
            is_active=True,
            publish_date="2025-01-01"
        )
        self.assertEqual(topic.title, "Test Debate Topic")
        self.assertTrue(topic.is_active)
        self.assertEqual(str(topic), "Test Debate Topic")

class FeaturedDebateModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="featured_user", password="pass123", email="featured_user@example.com"
        )
        self.topic = DebateTopic.objects.create(
            title="Featured Debate Topic",
            description="Topic to be featured.",
            is_active=True,
            publish_date="2025-01-01"
        )
    
    def test_create_featured_debate(self):
        featured = FeaturedDebate.objects.create(
            debate_topic=self.topic,
            display_order=1,
            active=True
        )
        self.assertEqual(featured.debate_topic, self.topic)
        self.assertEqual(featured.display_order, 1)
        self.assertTrue(featured.active)
        # Assuming __str__ returns something that includes "Featured"
        self.assertIn("Featured", str(featured))

class PersonalizedRecommendationModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="recommend_user", password="pass123", email="recommend_user@example.com"
        )
        self.topic = DebateTopic.objects.create(
            title="Recommended Debate Topic",
            description="Topic for recommendation.",
            is_active=True,
            publish_date="2025-01-01"
        )
    
    def test_create_personalized_recommendation(self):
        recommendation = PersonalizedRecommendation.objects.create(
            user=self.user,
            debate_topic=self.topic,
            score=95.0
        )
        self.assertEqual(recommendation.user, self.user)
        self.assertEqual(recommendation.debate_topic, self.topic)
        self.assertEqual(recommendation.score, 95.0)
        self.assertIn(self.user.username, str(recommendation))

# --- API Tests ---

class DebateTopicAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_topic", password="apipass", email="api_topic@example.com"
        )
        self.client.login(username="api_topic", password="apipass")
        self.topic = DebateTopic.objects.create(
            title="API Debate Topic",
            description="Created via API.",
            is_active=True,
            publish_date="2025-02-01"
        )
    
    def test_list_debate_topics(self):
        url = reverse("debatetopic-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_debate_topic_api(self):
        url = reverse("debatetopic-list")
        data = {
            "title": "New API Debate Topic",
            "description": "Created via API POST.",
            "is_active": True,
            "publish_date": "2025-03-01"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DebateTopic.objects.filter(title="New API Debate Topic").count(), 1)

class FeaturedDebateAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_featured", password="apipass", email="api_featured@example.com"
        )
        self.client.login(username="api_featured", password="apipass")
        self.topic = DebateTopic.objects.create(
            title="API Featured Topic",
            description="Topic to be featured via API.",
            is_active=True,
            publish_date="2025-02-01"
        )
        self.featured = FeaturedDebate.objects.create(
            debate_topic=self.topic,
            display_order=1,
            active=True
        )
    
    def test_list_featured_debates(self):
        url = reverse("featureddebate-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_featured_debate_api(self):
        url = reverse("featureddebate-list")
        data = {
            "debate_topic": self.topic.id,
            "display_order": 2,
            "active": True
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FeaturedDebate.objects.filter(display_order=2).count(), 1)

class PersonalizedRecommendationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_recommend", password="apipass", email="api_recommend@example.com"
        )
        self.client.login(username="api_recommend", password="apipass")
        self.topic = DebateTopic.objects.create(
            title="API Recommendation Topic",
            description="Topic for recommendation via API.",
            is_active=True,
            publish_date="2025-02-01"
        )
        self.recommendation = PersonalizedRecommendation.objects.create(
            user=self.user,
            debate_topic=self.topic,
            score=88.0
        )
    
    def test_list_personalized_recommendations(self):
        url = reverse("personalizedrecommendation-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_personalized_recommendation_api(self):
        url = reverse("personalizedrecommendation-list")
        data = {
            "user": self.user.id,
            "debate_topic": self.topic.id,
            "score": 92.0
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PersonalizedRecommendation.objects.filter(score=92.0).count(), 1)
