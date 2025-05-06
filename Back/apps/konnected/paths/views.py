# apps/konnected/paths/views.py
from rest_framework import viewsets, permissions
from konnected.paths.models import LearningPath, PathStep
from konnected.paths.serializers import (
    LearningPathSerializer,
    PathStepSerializer
)

class LearningPathViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer la création et la modification des parcours d'apprentissage.
    """
    serializer_class = LearningPathSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les parcours créés par l'utilisateur connecté
        return LearningPath.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        # Associe automatiquement le créateur
        serializer.save(created_by=self.request.user)


class PathStepViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les étapes individuelles d'un parcours d'apprentissage.
    """
    serializer_class = PathStepSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les étapes des parcours de l'utilisateur
        return PathStep.objects.filter(
            learning_path__created_by=self.request.user
        )

    def perform_create(self, serializer):
        # On suppose que 'learning_path' est fourni dans request.data
        serializer.save()
