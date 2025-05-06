# apps/ethikos/debate_arena/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from ethikos.debate_arena.models import DebateSession, Argument, VoteRecord

User = get_user_model()

# --- Model Tests ---

class DebateSessionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="debate_mod", password="pass123", email="debate_mod@example.com"
        )
    
    def test_create_debate_session(self):
        session = DebateSession.objects.create(
            topic="Test Debate Session",
            description="A session for testing debate functionality.",
            moderator=self.user,
            start_time=timezone.now()
        )
        self.assertEqual(session.topic, "Test Debate Session")
        self.assertEqual(session.moderator, self.user)
        self.assertTrue(session.is_active)  # Assuming default is active
        self.assertIn("Test Debate Session", str(session))

class ArgumentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="arg_author", password="pass123", email="arg_author@example.com"
        )
        self.session = DebateSession.objects.create(
            topic="Debate on Technology",
            description="Debate session for technology topics.",
            moderator=self.user,
            start_time=timezone.now()
        )
    
    def test_create_argument(self):
        arg = Argument.objects.create(
            debate_session=self.session,
            author=self.user,
            content="This is a test argument."
        )
        self.assertEqual(arg.debate_session, self.session)
        self.assertEqual(arg.author, self.user)
        self.assertEqual(arg.content, "This is a test argument.")
        # Test threaded reply
        reply = Argument.objects.create(
            debate_session=self.session,
            author=self.user,
            content="This is a reply.",
            parent=arg
        )
        self.assertEqual(reply.parent, arg)
        self.assertEqual(reply.debate_session, self.session)

class VoteRecordModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="voter", password="pass123", email="voter@example.com"
        )
        self.session = DebateSession.objects.create(
            topic="Debate on Voting",
            description="Debate session for vote testing.",
            moderator=self.user,
            start_time=timezone.now()
        )
        self.argument = Argument.objects.create(
            debate_session=self.session,
            author=self.user,
            content="Argument to be voted on."
        )
    
    def test_create_vote_record(self):
        vote = VoteRecord.objects.create(
            argument=self.argument,
            voter=self.user,
            vote_value=1
        )
        self.assertEqual(vote.argument, self.argument)
        self.assertEqual(vote.voter, self.user)
        self.assertEqual(vote.vote_value, 1)
        self.assertIn("voter", str(vote))

# --- API Tests ---

class DebateSessionAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_debate", password="apipass", email="api_debate@example.com"
        )
        self.client.login(username="api_debate", password="apipass")
        self.session = DebateSession.objects.create(
            topic="API Debate Session",
            description="Session created via API.",
            moderator=self.user,
            start_time=timezone.now()
        )
    
    def test_list_debate_sessions(self):
        url = reverse("debatesession-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_debate_session_api(self):
        url = reverse("debatesession-list")
        data = {
            "topic": "New API Debate Session",
            "description": "Created via API POST.",
            "moderator": self.user.id,
            "start_time": timezone.now().isoformat()
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DebateSession.objects.filter(topic="New API Debate Session").count(), 1)
    
    def test_end_debate_session_action(self):
        # Test custom action: end_session
        url = reverse("debatesession-end-session", kwargs={"pk": self.session.pk})
        data = {"end_time": timezone.now().isoformat()}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.session.refresh_from_db()
        self.assertFalse(self.session.is_active)

class ArgumentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_arg", password="apipass", email="api_arg@example.com"
        )
        self.client.login(username="api_arg", password="apipass")
        self.session = DebateSession.objects.create(
            topic="API Debate for Arguments",
            description="Testing arguments via API.",
            moderator=self.user,
            start_time=timezone.now()
        )
    
    def test_create_argument_api(self):
        url = reverse("argument-list")
        data = {
            "debate_session": self.session.id,
            "author": self.user.id,
            "content": "API argument test",
            "parent": None,
            "vote_count": 0
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.session.arguments.count(), 1)

class VoteRecordAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_voter", password="apipass", email="api_voter@example.com"
        )
        self.client.login(username="api_voter", password="apipass")
        self.session = DebateSession.objects.create(
            topic="API Debate for Votes",
            description="Testing votes via API.",
            moderator=self.user,
            start_time=timezone.now()
        )
        self.argument = Argument.objects.create(
            debate_session=self.session,
            author=self.user,
            content="Argument for vote API"
        )
    
    def test_create_vote_record_api(self):
        url = reverse("voterecord-list")
        data = {
            "argument": self.argument.id,
            "voter": self.user.id,
            "vote_value": -1
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.argument.vote_records.count(), 1)
