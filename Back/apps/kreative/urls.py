# apps/kreative/artworks/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kreative.artworks.views import ExhibitionViewSet, ArtworkViewSet

app_name = "artworks"

router = DefaultRouter()
router.register(r"exhibitions", ExhibitionViewSet)
router.register(r"artworks",    ArtworkViewSet)

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
