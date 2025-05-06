# apps/keenkonnect/projects/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.projects.views import ProjectViewSet, MilestoneViewSet, TaskViewSet

app_name = "projects"

router = DefaultRouter()
router.register(r"projects",   ProjectViewSet)
router.register(r"milestones", MilestoneViewSet)
router.register(r"tasks",      TaskViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
