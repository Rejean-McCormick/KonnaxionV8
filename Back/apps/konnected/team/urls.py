# apps/konnected/team/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.team.views import TeamViewSet, TeamInvitationViewSet

app_name = "team"

router = DefaultRouter()
router.register(r"teams",       TeamViewSet,             basename="team")
router.register(r"invitations", TeamInvitationViewSet,  basename="teaminvitation")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
