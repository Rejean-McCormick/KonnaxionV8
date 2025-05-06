"""
File: apps/ethikos/ethikos_prioritization/models.py

This module develops models to rank and filter debates based on engagement,
credibility, and reputation integration.
"""

from django.db import models
from common.base_models import BaseModel

class DebatePrioritization(BaseModel):
    """
    Ranks a debate session based on computed criteria.
    """
    debate_session = models.ForeignKey(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="prioritizations",
        help_text="Debate session being ranked"
    )
    ranking_score = models.FloatField(help_text="Computed ranking score for the debate")
    criteria = models.JSONField(null=True, blank=True, help_text="JSON data detailing the ranking criteria")
    notes = models.TextField(null=True, blank=True, help_text="Additional notes or rationale for the ranking")

    def __str__(self):
        return f"Prioritization for {self.debate_session.topic}: Score {self.ranking_score}"
