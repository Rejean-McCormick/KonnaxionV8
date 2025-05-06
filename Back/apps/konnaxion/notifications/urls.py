# apps/konnaxion/notifications/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.notifications.views import NotificationViewSet

app_name = "notifications"

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]
