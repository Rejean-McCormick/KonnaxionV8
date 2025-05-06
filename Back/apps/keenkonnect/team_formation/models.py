"""
File: apps/keenkonnect/keenTeamFormation/models.py

This module defines models for AI-driven team formation.
It captures team formation requests and candidate evaluations with computed compatibility scores.
"""

from django.db import models
from common.base_models import BaseModel

class TeamFormationRequest(BaseModel):
    """
    Represents a request to form a team for a project.
    """
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="team_formation_requests",
        help_text="Project for which the team is being formed."
    )
    requested_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="team_formation_requests",
        help_text="User who initiated the team formation request."
    )
    required_roles = models.JSONField(null=True, blank=True, help_text="JSON specifying required roles and skills.")
    additional_info = models.TextField(null=True, blank=True, help_text="Additional information about the request.")

    def __str__(self):
        return f"Team Formation Request for {self.project.title}"

class TeamFormationCandidate(BaseModel):
    """
    Represents a candidate for team formation, with a computed compatibility score.
    """
    formation_request = models.ForeignKey(
        TeamFormationRequest,
        on_delete=models.CASCADE,
        related_name="candidates",
        help_text="Associated team formation request."
    )
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="team_formation_candidates",
        help_text="User being considered for the team."
    )
    skills = models.JSONField(null=True, blank=True, help_text="JSON data representing the user's skills.")
    compatibility_score = models.FloatField(default=0, help_text="Computed compatibility score.")

    def __str__(self):
        return f"Candidate {self.user} - Score: {self.compatibility_score}"
