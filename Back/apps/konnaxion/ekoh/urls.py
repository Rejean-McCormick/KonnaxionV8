# apps/konnaxion/ekoh/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.ekoh.views import (
    ExpertiseTagViewSet,
    ReputationProfileViewSet,
    ReputationEventViewSet,
    WeightedVoteViewSet,
)

app_name = "ekoh"

router = DefaultRouter()
router.register(r"expertise-tags",      ExpertiseTagViewSet,       basename="expertise-tag")
router.register(r"reputation-profiles",  ReputationProfileViewSet,   basename="reputation-profile")
router.register(r"reputation-events",    ReputationEventViewSet,     basename="reputation-event")
router.register(r"weighted-votes",       WeightedVoteViewSet,        basename="weighted-vote")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
