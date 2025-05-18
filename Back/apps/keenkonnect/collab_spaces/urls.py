from django.urls import path, include
from rest_framework.routers import DefaultRouter
from keenkonnect.collab_spaces.views import (
    CollabSpaceViewSet,
    DocumentViewSet,
    ChatMessageViewSet,
)

app_name = "collab_spaces"

router = DefaultRouter()
router.register(
    r"collab_spaces",
    CollabSpaceViewSet,
    basename="collab-space",
)
router.register(
    r"documents",
    DocumentViewSet,
    basename="document",
)
router.register(
    r"chat_messages",
    ChatMessageViewSet,
    basename="chat-message",
)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
