# apps/keenkonnect/projects/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.projects.views import ProjectViewSet, MilestoneViewSet, TaskViewSet

app_name = "projects"

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"milestones", MilestoneViewSet, basename="milestone")
router.register(r"tasks", TaskViewSet, basename="task")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
