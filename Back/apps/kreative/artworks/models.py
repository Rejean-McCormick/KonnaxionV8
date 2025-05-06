"""
File: apps\kreative\artworks\models.py

Purpose:
Build models for the artwork catalog, including fields for media uploads, metadata,
and exhibition details.
"""

from django.db import models
from common.base_models import BaseModel

class Exhibition(BaseModel):
    """
    Represents an exhibition event for displaying artworks.
    """
    name = models.CharField(max_length=255, help_text="Name of the exhibition")
    description = models.TextField(null=True, blank=True, help_text="Description of the exhibition")
    start_date = models.DateField(null=True, blank=True, help_text="Exhibition start date")
    end_date = models.DateField(null=True, blank=True, help_text="Exhibition end date")
    location = models.CharField(max_length=255, null=True, blank=True, help_text="Location of the exhibition")

    def __str__(self):
        return self.name

class Artwork(BaseModel):
    """
    Represents an individual artwork in the catalog.
    """
    title = models.CharField(max_length=255, help_text="Title of the artwork")
    description = models.TextField(help_text="Description of the artwork")
    image = models.ImageField(upload_to="artworks/", help_text="Image of the artwork")
    metadata = models.JSONField(null=True, blank=True, help_text="Additional metadata (e.g., dimensions, medium)")
    exhibition = models.ForeignKey(
        Exhibition,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="artworks",
        help_text="Exhibition where the artwork is displayed"
    )

    def __str__(self):
        return self.title
