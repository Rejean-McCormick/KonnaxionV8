# apps/keenkonnect/knowledge_hub/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from keenkonnect.knowledge_hub.models import KnowledgeDocument, DocumentRevision

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class KnowledgeDocumentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="kh_user", password="pass123", email="kh_user@example.com"
        )

    def test_create_knowledge_document(self):
        """
        Teste la création d'une instance de KnowledgeDocument.
        Vérifie que les champs (titre, description, document_file, version et created_by)
        sont correctement enregistrés et que la représentation en chaîne est conforme.
        """
        doc = KnowledgeDocument.objects.create(
            title="Test Document",
            description="Un document de test pour le knowledge hub.",
            document_file="knowledge_documents/test_doc.pdf",
            version="1.0",
            created_by=self.user
        )
        self.assertEqual(doc.title, "Test Document")
        self.assertEqual(doc.description, "Un document de test pour le knowledge hub.")
        self.assertEqual(doc.document_file, "knowledge_documents/test_doc.pdf")
        self.assertEqual(doc.version, "1.0")
        self.assertEqual(doc.created_by, self.user)
        # Supposons que __str__ retourne "Test Document (v1.0)"
        expected_str = f"{doc.title} (v{doc.version})"
        self.assertEqual(str(doc), expected_str)


class DocumentRevisionModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="rev_user", password="pass123", email="rev_user@example.com"
        )
        self.doc = KnowledgeDocument.objects.create(
            title="Revision Test Document",
            description="Document pour tester les révisions.",
            document_file="knowledge_documents/rev_test.pdf",
            version="1.0",
            created_by=self.user
        )

    def test_create_document_revision(self):
        """
        Teste la création d'une révision pour un document de connaissances.
        Vérifie que les champs (knowledge_document, revision_number, changes, revised_by)
        sont correctement enregistrés et que la représentation en chaîne est conforme.
        """
        revision = DocumentRevision.objects.create(
            knowledge_document=self.doc,
            revision_number="1.1",
            changes="Mise à jour du contenu initial.",
            revised_by=self.user
        )
        self.assertEqual(revision.knowledge_document, self.doc)
        self.assertEqual(revision.revision_number, "1.1")
        self.assertEqual(revision.changes, "Mise à jour du contenu initial.")
        self.assertEqual(revision.revised_by, self.user)
        # Supposons que __str__ retourne "Revision Test Document Revision 1.1"
        expected_str = f"{self.doc.title} Revision {revision.revision_number}"
        self.assertEqual(str(revision), expected_str)


# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class KnowledgeDocumentAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié et une instance initiale de KnowledgeDocument pour tester l'API.
        """
        self.user = User.objects.create_user(
            username="api_kh", password="apipass", email="api_kh@example.com"
        )
        self.client.login(username="api_kh", password="apipass")
        self.document = KnowledgeDocument.objects.create(
            title="API Knowledge Document",
            description="Document créé via l'API pour le knowledge hub.",
            document_file="knowledge_documents/api_doc.pdf",
            version="1.0",
            created_by=self.user
        )

    def test_list_knowledge_documents(self):
        """
        Vérifie que l'API retourne la liste des KnowledgeDocument.
        On suppose que le basename dans le routeur DRF est "knowledgedocument".
        """
        url = reverse("knowledgedocument-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_knowledge_document_api(self):
        """
        Vérifie la création d'une nouvelle instance de KnowledgeDocument via l'API.
        """
        url = reverse("knowledgedocument-list")
        data = {
            "title": "New API Knowledge Document",
            "description": "Document créé via l'API.",
            "document_file": "knowledge_documents/new_api_doc.pdf",
            "version": "1.0",
            "created_by": self.user.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(KnowledgeDocument.objects.filter(title="New API Knowledge Document").count(), 1)


class DocumentRevisionAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur authentifié, un KnowledgeDocument et une révision initiale pour tester l'API des révisions.
        """
        self.user = User.objects.create_user(
            username="api_rev", password="apipass", email="api_rev@example.com"
        )
        self.client.login(username="api_rev", password="apipass")
        self.document = KnowledgeDocument.objects.create(
            title="API Document for Revision",
            description="Document pour tester les révisions via l'API.",
            document_file="knowledge_documents/api_rev.pdf",
            version="1.0",
            created_by=self.user
        )
        self.revision = DocumentRevision.objects.create(
            knowledge_document=self.document,
            revision_number="1.1",
            changes="Première révision via l'API.",
            revised_by=self.user
        )

    def test_list_document_revisions(self):
        """
        Vérifie que l'API retourne la liste des révisions de documents.
        On suppose que le basename dans le routeur DRF est "documentrevision".
        """
        url = reverse("documentrevision-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_document_revision_api(self):
        """
        Vérifie la création d'une nouvelle révision via l'API.
        """
        url = reverse("documentrevision-list")
        data = {
            "knowledge_document": self.document.id,
            "revision_number": "1.2",
            "changes": "Deuxième révision via l'API.",
            "revised_by": self.user.id
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DocumentRevision.objects.filter(revision_number="1.2").count(), 1)
