# apps/kreative/marketplace/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from kreative.marketplace.views import (
    ArtistProfileViewSet,
    CommissionViewSet,
    MarketplaceListingViewSet,
)

app_name = "marketplace"

router = DefaultRouter()
router.register(r"artist_profiles", ArtistProfileViewSet, basename="artist_profiles")
router.register(r"commissions", CommissionViewSet, basename="commissions")
router.register(r"marketplace_listings", MarketplaceListingViewSet, basename="marketplace_listings")

urlpatterns = [
    path("", include((router.urls, app_name), namespace=app_name)),
]
