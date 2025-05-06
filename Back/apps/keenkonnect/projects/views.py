# apps/keenkonnect/projects/views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from keenkonnect.projects.models import Project, Milestone, Task
from keenkonnect.projects.serializers import (
    ProjectSerializer,
    MilestoneSerializer,
    TaskSerializer
)

class ProjectViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les projets collaboratifs.
    """
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les projets dont on est propriétaire
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Crée le projet et l'associe au propriétaire
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def change_status(self, request, pk=None):
        """
        Modifie le statut d'un projet (e.g. 'planning', 'in_progress', 'completed').
        """
        project = self.get_object()
        new_status = request.data.get('status')
        if not new_status:
            return Response({'error': 'Le champ "status" est requis.'},
                            status=status.HTTP_400_BAD_REQUEST)
        project.status = new_status
        project.save()
        return Response(self.get_serializer(project).data)


class MilestoneViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les jalons d'un projet.
    """
    serializer_class = MilestoneSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seuls les jalons des projets dont on est propriétaire
        return Milestone.objects.filter(project__owner=self.request.user)

    def perform_create(self, serializer):
        # S'assure que 'project' appartient bien à request.user dans le payload
        serializer.save()


class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les tâches d'un jalon de projet.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Seules les tâches des projets dont on est propriétaire
        return Task.objects.filter(milestone__project__owner=self.request.user)

    def perform_create(self, serializer):
        # On peut assigner automatiquement un utilisateur ou laisser via request.data
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def mark_completed(self, request, pk=None):
        """
        Marque une tâche comme complétée.
        """
        task = self.get_object()
        task.is_completed = True
        task.save()
        return Response(self.get_serializer(task).data)
