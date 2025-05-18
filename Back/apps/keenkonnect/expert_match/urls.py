from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.expert_match.views import (
    ExpertMatchRequestViewSet,
    CandidateProfileViewSet,
    MatchScoreViewSet,
)

app_name = "expert_match"

router = DefaultRouter()
router.register(
    r"expert_match_requests",
    ExpertMatchRequestViewSet,
    basename="expert-match-request",
)
router.register(
    r"candidate_profiles",
    CandidateProfileViewSet,
    basename="candidate-profile",
)
router.register(
    r"match_scores",
    MatchScoreViewSet,
    basename="match-score",
)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
