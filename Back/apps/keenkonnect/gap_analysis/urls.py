# apps/keenkonnect/gap_analysis/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.gap_analysis.views import GapAnalysisViewSet

app_name = "gap_analysis"

router = DefaultRouter()
router.register(r"gap_analyses", GapAnalysisViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
