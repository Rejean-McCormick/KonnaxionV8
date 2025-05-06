"""
File: apps/konnected/foundation/models.py

This module manages the core educational content (“Knowledge Units”).
It includes models for storing rich text, multimedia, and resource attachments,
with support for versioning and audit trails.
"""

from django.db import models
from common.base_models import BaseModel

class KnowledgeUnit(BaseModel):
    """
    Represents a unit of educational content.
    """
    title = models.CharField(max_length=255, help_text="Title of the knowledge unit.")
    content = models.TextField(help_text="Rich text content of the knowledge unit.")
    attachments = models.JSONField(
        null=True,
        blank=True,
        help_text="JSON list of attachment URLs or metadata."
    )
    language = models.CharField(
        max_length=10,
        default="en",
        help_text="Language code for the content."
    )
    version = models.PositiveIntegerField(
        default=1,
        help_text="Version number of the knowledge unit."
    )

    def __str__(self):
        return self.title
