# apps/ethikos/prioritization/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.prioritization.views import DebatePrioritizationViewSet

app_name = "prioritization"

router = DefaultRouter()
router.register(r"debate_prioritizations", DebatePrioritizationViewSet, basename="debateprioritization")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
