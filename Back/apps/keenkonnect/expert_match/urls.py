# apps/keenkonnect/expert_match/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.expert_match.views import (
    ExpertMatchRequestViewSet,
    CandidateProfileViewSet,
    MatchScoreViewSet,
)

app_name = "expert_match"

router = DefaultRouter()
router.register(r"expert_match_requests", ExpertMatchRequestViewSet)
router.register(r"candidate_profiles",    CandidateProfileViewSet)
router.register(r"match_scores",          MatchScoreViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
