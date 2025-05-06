from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.ai.views import AIResultViewSet

app_name = 'ai'

router = DefaultRouter()
router.register(r'results', AIResultViewSet, basename='airesult')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]
