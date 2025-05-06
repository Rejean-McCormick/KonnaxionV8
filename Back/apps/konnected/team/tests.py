# apps/konnected/team/tests.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from konnected.team.models import Team, TeamInvitation

User = get_user_model()

# ------------------------------------------------------------------------------
# 1. Tests des modèles (Model Tests)
# ------------------------------------------------------------------------------

class TeamModelTests(TestCase):
    def setUp(self):
        # Création de deux utilisateurs pour servir de membres
        self.user1 = User.objects.create_user(
            username="teamuser1", password="pass123", email="teamuser1@example.com"
        )
        self.user2 = User.objects.create_user(
            username="teamuser2", password="pass123", email="teamuser2@example.com"
        )

    def test_create_team(self):
        """
        Crée une équipe, y ajoute des membres et vérifie que :
         - Le nom et la description sont correctement enregistrés.
         - Le nombre de membres est correct.
         - La représentation en chaîne (méthode __str__) renvoie le nom de l'équipe.
        """
        team = Team.objects.create(name="Alpha Team", description="Description de l'équipe Alpha")
        team.members.add(self.user1, self.user2)
        self.assertEqual(team.name, "Alpha Team")
        self.assertEqual(team.description, "Description de l'équipe Alpha")
        self.assertEqual(team.members.count(), 2)
        self.assertEqual(str(team), "Alpha Team")


class TeamInvitationModelTests(TestCase):
    def setUp(self):
        # Création d'un utilisateur qui invite et d'un utilisateur invité
        self.inviter = User.objects.create_user(
            username="inviter", password="pass123", email="inviter@example.com"
        )
        self.invitee = User.objects.create_user(
            username="invitee", password="pass123", email="invitee@example.com"
        )
        # Création d'une équipe et ajout de l'inviteur comme membre
        self.team = Team.objects.create(name="Beta Team", description="Description de Beta Team")
        self.team.members.add(self.inviter)

    def test_create_team_invitation(self):
        """
        Crée une invitation pour rejoindre une équipe et vérifie que :
         - La relation avec l'équipe et l'utilisateur invité est correcte.
         - Le statut et le message sont enregistrés correctement.
         - La représentation en chaîne renvoie la chaîne attendue.
        """
        invitation = TeamInvitation.objects.create(
            team=self.team,
            invited_user=self.invitee,
            status="pending",
            message="Rejoignez notre équipe !"
        )
        self.assertEqual(invitation.team, self.team)
        self.assertEqual(invitation.invited_user, self.invitee)
        self.assertEqual(invitation.status, "pending")
        self.assertEqual(invitation.message, "Rejoignez notre équipe !")
        expected_str = f"Invitation for {self.invitee} to join {self.team.name} [pending]"
        self.assertEqual(str(invitation), expected_str)


# ------------------------------------------------------------------------------
# 2. Tests des endpoints API (API Tests)
# ------------------------------------------------------------------------------

class TeamAPITests(APITestCase):
    def setUp(self):
        """
        Crée deux utilisateurs et authentifie le premier pour tester les endpoints liés aux équipes.
        """
        self.user1 = User.objects.create_user(
            username="api_teamuser1", password="apipass", email="api_teamuser1@example.com"
        )
        self.user2 = User.objects.create_user(
            username="api_teamuser2", password="apipass", email="api_teamuser2@example.com"
        )
        self.client.login(username="api_teamuser1", password="apipass")
        self.team = Team.objects.create(name="Gamma Team", description="Équipe créée via l'API")
        self.team.members.add(self.user1)

    def test_list_teams(self):
        """
        Vérifie que l'API retourne la liste des équipes auxquelles l'utilisateur authentifié participe.
        On suppose que le basename dans le routeur DRF est "team".
        """
        url = reverse("team-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_team_via_api(self):
        """
        Vérifie que l'on peut créer une nouvelle équipe via l'API.
        Les membres de l'équipe sont spécifiés par leurs identifiants.
        """
        url = reverse("team-list")
        data = {
            "name": "Delta Team",
            "description": "Équipe créée via l'API",
            "members": [self.user1.id, self.user2.id]
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Team.objects.filter(name="Delta Team").count(), 1)


class TeamInvitationAPITests(APITestCase):
    def setUp(self):
        """
        Crée un utilisateur qui invite et un utilisateur invité,
        puis authentifie l'inviteur pour tester les endpoints des invitations.
        """
        self.inviter = User.objects.create_user(
            username="api_inviter", password="apipass", email="api_inviter@example.com"
        )
        self.invitee = User.objects.create_user(
            username="api_invitee", password="apipass", email="api_invitee@example.com"
        )
        self.client.login(username="api_inviter", password="apipass")
        self.team = Team.objects.create(name="Epsilon Team", description="Équipe pour les invitations API")
        self.team.members.add(self.inviter)

    def test_list_team_invitations(self):
        """
        Vérifie que l'API retourne la liste des invitations envoyées.
        On suppose que le basename dans le routeur DRF est "teaminvitation".
        """
        # Création d'une invitation
        TeamInvitation.objects.create(
            team=self.team,
            invited_user=self.invitee,
            status="pending",
            message="Invitation via API"
        )
        url = reverse("teaminvitation-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_team_invitation_via_api(self):
        """
        Vérifie que l'on peut créer une invitation via l'API.
        """
        url = reverse("teaminvitation-list")
        data = {
            "team": self.team.id,
            "invited_user": self.invitee.id,
            "status": "pending",
            "message": "Invitation créée via l'API"
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TeamInvitation.objects.filter(team=self.team, invited_user=self.invitee).count(), 1)
