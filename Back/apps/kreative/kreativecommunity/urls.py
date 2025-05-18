# apps/kreative/kreativecommunity/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kreative.kreativecommunity.views import (
    DiscussionThreadViewSet,
    CommentViewSet,
)

app_name = "kreativecommunity"

router = DefaultRouter()
router.register(r"discussions", DiscussionThreadViewSet, basename="discussions")
router.register(r"comments", CommentViewSet, basename="comments")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
