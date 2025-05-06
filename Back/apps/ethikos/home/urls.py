# apps/ethikos/home/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.home.views import (
    DebateTopicViewSet,
    FeaturedDebateViewSet,
    PersonalizedRecommendationViewSet,
)

app_name = "home"

router = DefaultRouter()
router.register(r'debate_topics',                DebateTopicViewSet)
router.register(r'featured_debates',             FeaturedDebateViewSet)
router.register(r'personalized_recommendations', PersonalizedRecommendationViewSet)

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]
