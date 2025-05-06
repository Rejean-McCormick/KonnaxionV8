# apps/keenkonnect/team_formation/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.team_formation.views import (
    TeamFormationRequestViewSet,
    TeamFormationCandidateViewSet,
)

app_name = "team_formation"

router = DefaultRouter()
router.register(r"team_formation_requests",   TeamFormationRequestViewSet)
router.register(r"team_formation_candidates", TeamFormationCandidateViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
