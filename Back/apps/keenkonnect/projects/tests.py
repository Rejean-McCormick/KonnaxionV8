# apps/keenkonnect/projects/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone

from rest_framework import status
from rest_framework.test import APITestCase

from keenkonnect.projects.models import Project, Milestone, Task

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests Unitaires des Modèles
# ------------------------------------------------------------------------------

class ProjectModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="proj_user", password="pass123", email="proj_user@example.com"
        )
    
    def test_create_project(self):
        """
        Vérifie la création d'un projet et la bonne affectation de ses champs.
        On s'attend à ce que la représentation en chaîne retourne le titre du projet.
        """
        project = Project.objects.create(
            title="Test Project",
            description="Un projet de test pour KeenKonnect.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.assertEqual(project.title, "Test Project")
        self.assertEqual(project.description, "Un projet de test pour KeenKonnect.")
        self.assertEqual(project.owner, self.user)
        self.assertEqual(project.status, "planning")
        # Supposons que __str__ retourne le titre du projet.
        self.assertEqual(str(project), "Test Project")


class MilestoneModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="milestone_user", password="pass123", email="milestone_user@example.com"
        )
        self.project = Project.objects.create(
            title="Milestone Project",
            description="Projet pour tester les jalons.",
            owner=self.user,
            progress=0,
            status="planning"
        )
    
    def test_create_milestone(self):
        """
        Vérifie la création d'une étape (Milestone) associée à un projet.
        La représentation en chaîne est supposée être du type:
        "<Project.title> - <Milestone.title>"
        """
        milestone = Milestone.objects.create(
            project=self.project,
            title="First Milestone",
            description="Première étape du projet.",
            due_date="2025-03-01",
            status="pending"
        )
        self.assertEqual(milestone.title, "First Milestone")
        self.assertEqual(milestone.project, self.project)
        expected_str = f"{self.project.title} - {milestone.title}"
        self.assertEqual(str(milestone), expected_str)


class TaskModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="task_user", password="pass123", email="task_user@example.com"
        )
        self.project = Project.objects.create(
            title="Task Project",
            description="Projet pour tester les tâches.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.milestone = Milestone.objects.create(
            project=self.project,
            title="Task Milestone",
            description="Jalon pour les tâches.",
            due_date="2025-04-01",
            status="pending"
        )
    
    def test_create_task(self):
        """
        Vérifie la création d'une tâche associée à un jalon.
        Teste que le titre, la description, la date d'échéance, et le statut d'achèvement sont corrects.
        """
        task = Task.objects.create(
            milestone=self.milestone,
            title="Test Task",
            description="Description de la tâche de test.",
            assigned_to=self.user,
            due_date="2025-03-15",
            is_completed=False
        )
        self.assertEqual(task.title, "Test Task")
        self.assertEqual(task.milestone, self.milestone)
        self.assertFalse(task.is_completed)
        # Supposons que __str__ inclut le titre de la tâche.
        self.assertIn("Test Task", str(task))

# ------------------------------------------------------------------------------
# 2. Tests des Endpoints API
# ------------------------------------------------------------------------------

class ProjectAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_proj", password="apipass", email="api_proj@example.com"
        )
        self.client.login(username="api_proj", password="apipass")
        self.project = Project.objects.create(
            title="API Project",
            description="Projet créé via l'API.",
            owner=self.user,
            progress=0,
            status="planning"
        )
    
    def test_list_projects(self):
        """
        Vérifie que l'API retourne la liste des projets.
        On suppose que le basename configuré dans le routeur DRF est "project".
        """
        url = reverse("project-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_project_api(self):
        """
        Vérifie la création d'un projet via l'API.
        """
        url = reverse("project-list")
        data = {
            "title": "New API Project",
            "description": "Projet créé via l'API.",
            "owner": self.user.id,
            "progress": 0,
            "status": "planning"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.filter(title="New API Project").count(), 1)
    
    def test_change_project_status(self):
        """
        Vérifie l'action personnalisée pour modifier le statut d'un projet.
        On suppose que le ViewSet expose une action 'change_status' accessible via l'URL nommée "project-change-status".
        """
        url = reverse("project-change-status", kwargs={"pk": self.project.pk})
        data = {"status": "in_progress"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.status, "in_progress")


class MilestoneAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_milestone", password="apipass", email="api_milestone@example.com"
        )
        self.client.login(username="api_milestone", password="apipass")
        self.project = Project.objects.create(
            title="API Project for Milestones",
            description="Projet pour tester l'API des jalons.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.milestone = Milestone.objects.create(
            project=self.project,
            title="Initial Milestone",
            description="Premier jalon.",
            due_date="2025-03-10",
            status="pending"
        )
    
    def test_list_milestones(self):
        """
        Vérifie que l'API retourne la liste des jalons pour un projet donné.
        On suppose que l'URL est imbriquée avec un paramètre 'project_pk'.
        """
        url = reverse("milestone-list", kwargs={"project_pk": self.project.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_milestone_api(self):
        """
        Vérifie la création d'un jalon via l'API.
        """
        url = reverse("milestone-list", kwargs={"project_pk": self.project.pk})
        data = {
            "project": self.project.id,
            "title": "New Milestone",
            "description": "Jalon créé via l'API.",
            "due_date": "2025-03-20",
            "status": "pending"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Milestone.objects.filter(title="New Milestone").count(), 1)


class TaskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="api_task", password="apipass", email="api_task@example.com"
        )
        self.client.login(username="api_task", password="apipass")
        self.project = Project.objects.create(
            title="API Project for Tasks",
            description="Projet pour tester l'API des tâches.",
            owner=self.user,
            progress=0,
            status="planning"
        )
        self.milestone = Milestone.objects.create(
            project=self.project,
            title="Task Milestone",
            description="Jalon pour les tâches.",
            due_date="2025-03-25",
            status="pending"
        )
        self.task = Task.objects.create(
            milestone=self.milestone,
            title="Initial Task",
            description="Tâche initiale.",
            assigned_to=self.user,
            due_date="2025-03-15",
            is_completed=False
        )
    
    def test_list_tasks(self):
        """
        Vérifie que l'API retourne la liste des tâches pour un jalon donné.
        On suppose que l'URL est imbriquée avec un paramètre 'milestone_pk'.
        """
        url = reverse("task-list", kwargs={"milestone_pk": self.milestone.pk})
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
    
    def test_create_task_api(self):
        """
        Vérifie la création d'une tâche via l'API.
        """
        url = reverse("task-list", kwargs={"milestone_pk": self.milestone.pk})
        data = {
            "milestone": self.milestone.id,
            "title": "New API Task",
            "description": "Tâche créée via l'API.",
            "assigned_to": self.user.id,
            "due_date": "2025-03-18",
            "is_completed": False
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.filter(title="New API Task").count(), 1)
    
    def test_mark_task_completed(self):
        """
        Vérifie l'action personnalisée pour marquer une tâche comme complétée.
        On suppose que le ViewSet des tâches expose une action 'mark_completed'
        accessible via une URL nommée "task-mark-completed".
        """
        url = reverse("task-mark-completed", kwargs={"pk": self.task.pk})
        response = self.client.post(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertTrue(self.task.is_completed)
