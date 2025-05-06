# apps/konnaxion/search/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

# Importation des modèles du module search
from konnaxion.search.models import SearchIndex, SearchQueryLog

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests des modèles (Model Tests)
# ------------------------------------------------------------------------------

class SearchIndexModelTests(TestCase):
    def test_create_search_index(self):
        """
        Vérifie la création d'une instance de SearchIndex.
        On s'assure que le nom et la configuration sont correctement enregistrés.
        """
        index = SearchIndex.objects.create(
            name="TestIndex",
            settings='{"analyzer": "standard"}'
        )
        self.assertEqual(index.name, "TestIndex")
        # Vérifier que la chaîne 'standard' figure dans la configuration
        self.assertIn("standard", index.settings)


class SearchQueryLogModelTests(TestCase):
    def test_create_search_query_log(self):
        """
        Vérifie la création d'une instance de SearchQueryLog.
        On s'assure que le texte de la requête, le nombre de résultats et l'utilisateur associé
        sont correctement enregistrés.
        """
        user = User.objects.create_user(
            username="searcher",
            password="searchpass",
            email="searcher@example.com"
        )
        query_log = SearchQueryLog.objects.create(
            user=user,
            query_text="test search",
            results_count=5
        )
        self.assertEqual(query_log.query_text, "test search")
        self.assertEqual(query_log.results_count, 5)
        self.assertEqual(query_log.user, user)

# ------------------------------------------------------------------------------
# 2. Tests des endpoints API (API Tests)
# ------------------------------------------------------------------------------

class SearchIndexAPITests(APITestCase):
    def setUp(self):
        # Création et authentification d'un utilisateur de test
        self.user = User.objects.create_user(
            username="api_search",
            password="apipass",
            email="api_search@example.com"
        )
        self.client.login(username="api_search", password="apipass")
        # Création d'une instance de SearchIndex pour les tests d'API
        self.index = SearchIndex.objects.create(
            name="APITestIndex",
            settings='{"analyzer": "standard"}'
        )

    def test_list_search_indexes(self):
        """
        Vérifie que l'API renvoie la liste des index de recherche.
        On s'attend à obtenir au moins l'index créé dans setUp.
        """
        # On suppose que le basename utilisé dans le routeur DRF est "searchindex"
        url = reverse("searchindex-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # On vérifie que la liste contient au moins un élément
        self.assertGreaterEqual(len(response.data), 1)


class SearchQueryLogAPITests(APITestCase):
    def setUp(self):
        # Création et authentification d'un utilisateur de test
        self.user = User.objects.create_user(
            username="api_query",
            password="apipass",
            email="api_query@example.com"
        )
        self.client.login(username="api_query", password="apipass")
        # Création d'une instance de SearchQueryLog pour les tests d'API
        self.query_log = SearchQueryLog.objects.create(
            user=self.user,
            query_text="API test query",
            results_count=10
        )

    def test_list_search_query_logs(self):
        """
        Vérifie que l'API renvoie la liste des logs de requêtes de recherche.
        """
        # On suppose que le basename utilisé dans le routeur DRF est "searchquerylog"
        url = reverse("searchquerylog-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # On vérifie que la liste contient au moins un élément
        self.assertGreaterEqual(len(response.data), 1)
