"""
File: apps/konnected/offline/models.py

This module ensures that educational content is available offline.
It includes models for packaging content for offline consumption and tracking synchronization.
"""

from django.db import models
from common.base_models import BaseModel

class OfflineContentPackage(BaseModel):
    """
    Represents a packaged set of educational content for offline use.
    """
    title = models.CharField(max_length=255, help_text="Title of the offline content package.")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the offline package."
    )
    content_data = models.JSONField(help_text="JSON data representing the packaged content for offline use.")
    last_synced = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp of the last successful sync."
    )
    conflict_resolution_notes = models.TextField(
        null=True,
        blank=True,
        help_text="Notes on any conflicts during sync."
    )

    def __str__(self):
        return self.title
