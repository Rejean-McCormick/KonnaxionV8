# apps/konnected/konnectedcommunity/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnected.konnectedcommunity.views import (
    DiscussionThreadViewSet,
    CommentViewSet,
    CommunityPostViewSet,
    PostCommentViewSet,
)

app_name = "konnectedcommunity"

router = DefaultRouter()
router.register(
    r"discussion_threads",
    DiscussionThreadViewSet,
    basename="discussion_threads"
)
router.register(
    r"comments",
    CommentViewSet,
    basename="comments"
)
router.register(
    r"community_posts",
    CommunityPostViewSet,
    basename="community_posts"
)
router.register(
    r"post_comments",
    PostCommentViewSet,
    basename="post_comments"
)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
