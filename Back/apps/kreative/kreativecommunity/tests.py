# apps/konnected/community/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from konnected.konnectedcommunity.models import DiscussionThread, Comment

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class DiscussionThreadModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="comm_user", password="pass123", email="comm_user@example.com"
        )
    
    def test_create_discussion_thread(self):
        """
        Teste la création d'une instance de DiscussionThread.
        Vérifie que le titre, le contenu et l'auteur sont correctement enregistrés,
        et que la méthode __str__ retourne le titre.
        """
        thread = DiscussionThread.objects.create(
            title="Discussion de test",
            content="Ceci est le contenu de la discussion de test.",
            author=self.user
        )
        self.assertEqual(thread.title, "Discussion de test")
        self.assertEqual(thread.content, "Ceci est le contenu de la discussion de test.")
        self.assertEqual(thread.author, self.user)
        self.assertEqual(str(thread), "Discussion de test")


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="comm_user2", password="pass123", email="comm_user2@example.com"
        )
        self.thread = DiscussionThread.objects.create(
            title="Discussion pour commentaires",
            content="Contenu pour tester les commentaires.",
            author=self.user
        )
    
    def test_create_comment(self):
        """
        Teste la création d'un commentaire simple et d'une réponse (commentaire imbriqué).
        Vérifie que le commentaire est correctement associé au fil et que la relation parent/enfant fonctionne.
        """
        comment = Comment.objects.create(
            thread=self.thread,
            author=self.user,
            content="Ceci est un commentaire de test."
        )
        self.assertEqual(comment.thread, self.thread)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "Ceci est un commentaire de test.")
        # Vérification de la représentation en chaîne (elle doit contenir le username ou le titre du fil)
        self.assertIn(self.user.username, str(comment))
        
        # Création d'un commentaire réponse
        reply = Comment.objects.create(
            thread=self.thread,
            author=self.user,
            content="Ceci est une réponse au commentaire de test.",
            parent=comment
        )
        self.assertEqual(reply.parent, comment)
        self.assertEqual(reply.thread, self.thread)

# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class CommunityAPITests(APITestCase):
    def setUp(self):
        """
        Prépare un utilisateur authentifié et crée un fil de discussion ainsi qu'un commentaire
        initial pour tester les endpoints API du module community.
        """
        self.user = User.objects.create_user(
            username="api_comm", password="apipass", email="api_comm@example.com"
        )
        self.client.login(username="api_comm", password="apipass")
        
        # Création d'un fil de discussion via le modèle
        self.thread = DiscussionThread.objects.create(
            title="API Discussion Thread",
            content="Contenu créé via l'API pour le fil de discussion.",
            author=self.user
        )
        # Création d'un commentaire initial associé au fil
        self.comment = Comment.objects.create(
            thread=self.thread,
            author=self.user,
            content="Commentaire initial via l'API"
        )
    
    def test_list_discussion_threads(self):
        """
        Vérifie que l'API retourne la liste des fil de discussion.
        On suppose que le basename dans le routeur DRF est "discussionthread".
        """
        url = reverse("discussionthread-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Au moins le fil de discussion créé dans setUp doit être présent
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_discussion_thread_api(self):
        """
        Vérifie que l'on peut créer un nouveau fil de discussion via l'API.
        """
        url = reverse("discussionthread-list")
        data = {
            "title": "Nouvelle Discussion API",
            "content": "Contenu de la nouvelle discussion créée via l'API.",
            "author": self.user.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DiscussionThread.objects.filter(title="Nouvelle Discussion API").count(), 1)
    
    def test_list_comments(self):
        """
        Vérifie que l'API retourne la liste des commentaires pour un fil de discussion donné.
        Ici, on suppose que l'URL est configurée de manière imbriquée, par exemple :
        /api/discussionthreads/<discussion_pk>/comments/ avec le basename "comment".
        """
        url = reverse("comment-list", kwargs={"discussion_pk": self.thread.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Au moins le commentaire initial doit être présent
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_comment_api(self):
        """
        Vérifie que l'on peut créer un nouveau commentaire via l'API pour un fil de discussion donné.
        """
        url = reverse("comment-list", kwargs={"discussion_pk": self.thread.pk})
        data = {
            "thread": self.thread.id,
            "author": self.user.id,
            "content": "Nouveau commentaire via l'API"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.filter(content="Nouveau commentaire via l'API").count(), 1)
# apps/kreative/community/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from kreative.kreativecommunity.models import CommunityPost, PostComment

User = get_user_model()

# --- Model Tests ---

class CommunityPostModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="comm_post_user", password="pass123", email="comm_post_user@example.com")
    
    def test_create_community_post(self):
        post = CommunityPost.objects.create(
            title="Test Community Post",
            content="Content of the community post for testing.",
            posted_by=self.user
        )
        self.assertEqual(post.title, "Test Community Post")
        self.assertEqual(post.content, "Content of the community post for testing.")
        self.assertEqual(post.posted_by, self.user)
        self.assertIn("Test Community Post", str(post))

class PostCommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="comm_comment_user", password="pass123", email="comm_comment_user@example.com")
        self.post = CommunityPost.objects.create(
            title="Community Post for Comments",
            content="Testing comments on a community post.",
            posted_by=self.user
        )
    
    def test_create_post_comment(self):
        comment = PostComment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a test comment."
        )
        self.assertEqual(comment.post, self.post)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, "This is a test comment.")
        self.assertIn(self.user.username, str(comment))
        # Create a threaded reply
        reply = PostComment.objects.create(
            post=self.post,
            author=self.user,
            content="This is a reply to the test comment.",
            parent=comment
        )
        self.assertEqual(reply.parent, comment)
        self.assertEqual(reply.post, self.post)

# --- API Tests ---

class CommunityPostAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="api_comm_post", password="apipass", email="api_comm_post@example.com")
        self.client.login(username="api_comm_post", password="apipass")
        self.post = CommunityPost.objects.create(
            title="API Community Post",
            content="Community post created via API.",
            posted_by=self.user
        )
    
    def test_list_community_posts(self):
        url = reverse("communitypost-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_community_post_api(self):
        url = reverse("communitypost-list")
        data = {
            "title": "New API Community Post",
            "content": "Content created via API for community post.",
            "posted_by": self.user.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CommunityPost.objects.filter(title="New API Community Post").count(), 1)

class PostCommentAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="api_comm_comment", password="apipass", email="api_comm_comment@example.com")
        self.client.login(username="api_comm_comment", password="apipass")
        self.post = CommunityPost.objects.create(
            title="API Post for Comments",
            content="Testing API for post comments.",
            posted_by=self.user
        )
        self.comment = PostComment.objects.create(
            post=self.post,
            author=self.user,
            content="Initial comment via API."
        )
    
    def test_list_post_comments(self):
        # Assume the endpoint is nested: /api/community_posts/<post_pk>/comments/
        url = reverse("postcomment-list", kwargs={"post_pk": self.post.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_post_comment_api(self):
        url = reverse("postcomment-list", kwargs={"post_pk": self.post.pk})
        data = {
            "post": self.post.id,
            "author": self.user.id,
            "content": "New comment via API."
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostComment.objects.filter(content="New comment via API.").count(), 1)
