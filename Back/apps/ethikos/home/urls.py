from django.urls import path, include
from rest_framework.routers import DefaultRouter
from ethikos.home.views import (
    DebateCategoryViewSet,
    ResponseFormatViewSet,
    DebateTopicViewSet,
    FeaturedDebateViewSet,
    PersonalizedRecommendationViewSet,
    PublicVoteViewSet,
)

app_name = "home"

router = DefaultRouter()
router.register(r'debatecategory',    DebateCategoryViewSet,               basename='debate-category')
router.register(r'responseformat',    ResponseFormatViewSet,               basename='response-format')
router.register(r'debatetopic',       DebateTopicViewSet,                  basename='debate-topic')
router.register(r'featureddebate',    FeaturedDebateViewSet,               basename='featured-debate')
router.register(r'personalizedrec',   PersonalizedRecommendationViewSet,    basename='personalized-recommendation')
router.register(r'publicvote',        PublicVoteViewSet,                   basename='public-vote')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]
