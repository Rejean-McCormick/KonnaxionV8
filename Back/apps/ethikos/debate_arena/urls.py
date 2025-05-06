# apps/ethikos/debate_arena/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.debate_arena.views import (
    DebateSessionViewSet,
    ArgumentViewSet,
    VoteRecordViewSet,
)

app_name = "debate_arena"

router = DefaultRouter()
router.register(r"debate_sessions", DebateSessionViewSet, basename="debate-session")
router.register(r"arguments",       ArgumentViewSet,      basename="argument")
router.register(r"vote_records",    VoteRecordViewSet,    basename="voterecord")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
