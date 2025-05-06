# apps/konnaxion/search/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from konnaxion.search.views import SearchIndexViewSet, SearchQueryLogViewSet

app_name = "search"

router = DefaultRouter()
router.register(r'indexes',   SearchIndexViewSet,       basename='searchindex')
router.register(r'querylogs', SearchQueryLogViewSet,    basename='searchquerylog')

urlpatterns = [
    path('', include((router.urls, app_name), namespace=app_name)),
]
