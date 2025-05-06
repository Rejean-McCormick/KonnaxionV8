# apps/konnaxion/messaging/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.messaging.views import ConversationViewSet, MessageViewSet

app_name = "messaging"

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet, basename="conversation")
router.register(r"messages",      MessageViewSet,      basename="message")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
