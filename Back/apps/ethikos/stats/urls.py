# apps/ethikos/stats/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.stats.views import DebateStatisticViewSet, DebateEventLogViewSet

app_name = "stats"

router = DefaultRouter()
router.register(r"debate_statistics", DebateStatisticViewSet)
router.register(r"debate_event_logs", DebateEventLogViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
