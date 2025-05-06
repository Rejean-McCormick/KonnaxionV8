"""
File: apps/kreative/kreative_marketplace/models.py

Purpose:
Develop models for managing commissions, artist profiles, and marketplace listings.
Optionally includes placeholders for payment or contract integration.
"""

from django.db import models
from common.base_models import BaseModel

class ArtistProfile(BaseModel):
    """
    Represents an artist's profile containing portfolio and biography details.
    """
    user = models.OneToOneField(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="artist_profile",
        help_text="Associated user for the artist profile"
    )
    biography = models.TextField(null=True, blank=True, help_text="Artist biography")
    portfolio_url = models.URLField(null=True, blank=True, help_text="URL to the artist's portfolio")
    metadata = models.JSONField(null=True, blank=True, help_text="Additional artist metadata")

    def __str__(self):
        return f"Artist Profile: {self.user.username}"

class Commission(BaseModel):
    """
    Represents a commission request for custom artwork.
    """
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    title = models.CharField(max_length=255, help_text="Title of the commission")
    description = models.TextField(help_text="Details of the commission requirements")
    budget = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Budget for the commission")
    requested_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="commissions_requested",
        help_text="User requesting the commission"
    )
    assigned_to = models.ForeignKey(
        ArtistProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="commissions_assigned",
        help_text="Artist assigned to the commission"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="requested", help_text="Current status of the commission")
    # Placeholder for payment or contract integration
    contract_url = models.URLField(null=True, blank=True, help_text="URL for the commission contract or payment agreement")

    def __str__(self):
        return self.title

class MarketplaceListing(BaseModel):
    """
    Represents a marketplace listing for artworks available for sale or commission.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('sold', 'Sold'),
        ('removed', 'Removed'),
    ]
    title = models.CharField(max_length=255, help_text="Title of the listing")
    description = models.TextField(help_text="Description of the listing")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Price for the artwork")
    image = models.ImageField(upload_to="marketplace_listings/", help_text="Image for the listing")
    artist_profile = models.ForeignKey(
        ArtistProfile,
        on_delete=models.CASCADE,
        related_name="marketplace_listings",
        help_text="Artist profile associated with this listing"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active", help_text="Listing status")
    # Placeholder for future payment system integration
    payment_details = models.JSONField(null=True, blank=True, help_text="Payment details or integration data")

    def __str__(self):
        return self.title
