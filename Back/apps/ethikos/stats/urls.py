from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.stats.views import DebateStatisticViewSet, DebateEventLogViewSet

app_name = "stats"

router = DefaultRouter()
router.register(
    r"debate_statistics",
    DebateStatisticViewSet,
    basename="debate-statistic",
)
router.register(
    r"debate_event_logs",
    DebateEventLogViewSet,
    basename="debate-event-log",
)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
