from rest_framework import viewsets, permissions
from konnected.team.models import Team, TeamInvitation
from konnected.team.serializers import (
    TeamSerializer,
    TeamInvitationSerializer
)

class TeamViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer la création et la gestion des équipes éducatives.
    """
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les équipes où l'utilisateur est membre
        return Team.objects.filter(members=self.request.user)

    def perform_create(self, serializer):
        # Création + ajout automatique du créateur dans les membres
        team = serializer.save()
        team.members.add(self.request.user)


class TeamInvitationViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les invitations à rejoindre une équipe.
    """
    serializer_class = TeamInvitationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les invitations qui concernent l'utilisateur connecté
        return TeamInvitation.objects.filter(invited_user=self.request.user)
