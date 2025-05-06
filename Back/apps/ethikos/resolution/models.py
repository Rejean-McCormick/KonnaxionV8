"""
File: apps/ethikos/ethikos_resolution/models.py

This module defines models for documenting final debate resolutions.
It includes detailed decision histories and audit trails.
"""

from django.db import models
from common.base_models import BaseModel

class DebateResolution(BaseModel):
    """
    Documents the final resolution of a debate session.
    """
    debate_session = models.OneToOneField(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="resolution",
        help_text="Debate session for which this resolution applies"
    )
    resolution_text = models.TextField(help_text="Final resolution details and decisions")
    decision_history = models.JSONField(
        null=True,
        blank=True,
        help_text="JSON record of decision history and audit trail"
    )
    approved_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_resolutions",
        help_text="User who approved the resolution"
    )
    approved_at = models.DateTimeField(null=True, blank=True, help_text="Timestamp when the resolution was approved")

    def __str__(self):
        return f"Resolution for {self.debate_session.topic}"
