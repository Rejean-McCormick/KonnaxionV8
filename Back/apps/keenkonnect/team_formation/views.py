from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from keenkonnect.team_formation.models import (
    TeamFormationRequest,
    TeamFormationCandidate
)
from keenkonnect.team_formation.serializers import (
    TeamFormationRequestSerializer,
    TeamFormationCandidateSerializer
)
# Exemple : Importer une tâche asynchrone pour lancer la formation d'équipe
# from keenkonnect.team_formation.tasks import trigger_team_formation

class TeamFormationRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les demandes de formation d'équipe.
    """
    serializer_class = TeamFormationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les demandes initiées par l'utilisateur connecté
        return TeamFormationRequest.objects.filter(requested_by=self.request.user)

    def perform_create(self, serializer):
        # Création et association automatique à l'utilisateur
        serializer.save(requested_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def form_team(self, request, pk=None):
        """
        Action personnalisée pour déclencher le processus de formation d'équipe.
        """
        formation_request = self.get_object()
        # Si vous utilisez Celery : trigger_team_formation.delay(formation_request.id)
        return Response({
            "status": "Processus de formation déclenché",
            "request_id": formation_request.id
        })


class TeamFormationCandidateViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les candidats à la formation d'équipe.
    """
    serializer_class = TeamFormationCandidateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les candidats des demandes de l'utilisateur connecté
        return TeamFormationCandidate.objects.filter(
            formation_request__requested_by=self.request.user
        )

    # Si besoin, on peut surcharger perform_create pour valider la formation_request
    # def perform_create(self, serializer):
    #     serializer.save()
