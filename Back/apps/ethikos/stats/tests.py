# apps/ethikos/stats/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from ethikos.stats.models import DebateStatistic, DebateEventLog
from ethikos.debate_arena.models import DebateSession

User = get_user_model()

# --- Model Tests ---

class DebateStatisticModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="stat_user", password="pass123", email="stat_user@example.com")
        self.session = DebateSession.objects.create(
            topic="Statistic Debate",
            description="Debate session for statistics.",
            moderator=self.user,
            start_time=timezone.now()
        )
    
    def test_create_debate_statistic(self):
        stat = DebateStatistic.objects.create(
            debate_session=self.session,
            metric_name="total_votes",
            value=100.0
        )
        self.assertEqual(stat.debate_session, self.session)
        self.assertEqual(stat.metric_name, "total_votes")
        self.assertEqual(stat.value, 100.0)
        self.assertIn("total_votes", str(stat))

class DebateEventLogModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="event_user", password="pass123", email="event_user@example.com")
        self.session = DebateSession.objects.create(
            topic="Event Debate",
            description="Debate session for event logging.",
            moderator=self.user,
            start_time=timezone.now()
        )
    
    def test_create_debate_event_log(self):
        event_log = DebateEventLog.objects.create(
            debate_session=self.session,
            event_type="argument_posted",
            description="An argument was posted in the debate."
        )
        self.assertEqual(event_log.debate_session, self.session)
        self.assertEqual(event_log.event_type, "argument_posted")
        self.assertIn("argument_posted", str(event_log))

# --- API Tests ---

class DebateStatisticAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="api_stat", password="apipass", email="api_stat@example.com")
        self.client.login(username="api_stat", password="apipass")
        self.session = DebateSession.objects.create(
            topic="API Statistic Debate",
            description="Debate session for API statistics.",
            moderator=self.user,
            start_time=timezone.now()
        )
        self.stat = DebateStatistic.objects.create(
            debate_session=self.session,
            metric_name="active_participants",
            value=20.0
        )
    
    def test_list_debate_statistics(self):
        url = reverse("debatestatistic-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_debate_statistic_api(self):
        url = reverse("debatestatistic-list")
        data = {
            "debate_session": self.session.id,
            "metric_name": "average_score",
            "value": 75.0
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DebateStatistic.objects.filter(metric_name="average_score").count(), 1)

class DebateEventLogAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="api_event", password="apipass", email="api_event@example.com")
        self.client.login(username="api_event", password="apipass")
        self.session = DebateSession.objects.create(
            topic="API Event Debate",
            description="Debate session for API event logs.",
            moderator=self.user,
            start_time=timezone.now()
        )
        self.event_log = DebateEventLog.objects.create(
            debate_session=self.session,
            event_type="vote_cast",
            description="A vote was cast in the debate."
        )
    
    def test_list_debate_event_logs(self):
        url = reverse("debateeventlog-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_debate_event_log_api(self):
        url = reverse("debateeventlog-list")
        data = {
            "debate_session": self.session.id,
            "event_type": "comment_posted",
            "description": "A comment was posted in the debate."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DebateEventLog.objects.filter(event_type="comment_posted").count(), 1)
