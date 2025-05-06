"""
File: apps/keenkonnectexpert_match/models.py

This module defines models for matching projects with experts.
It includes models for match requests, candidate profiles, and compatibility scoring.
"""

from django.db import models
from common.base_models import BaseModel

class ExpertMatchRequest(BaseModel):
    """
    Represents a request for expert matching for a project.
    """
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="expert_match_requests",
        help_text="Project needing expert matching."
    )
    requested_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="expert_match_requests",
        help_text="User who initiated the match request."
    )
    description = models.TextField(help_text="Description of the expertise required.")
    criteria = models.JSONField(null=True, blank=True, help_text="JSON detailing matching criteria.")
    created_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the request was created.")

    def __str__(self):
        return f"Expert Match Request for {self.project.title}"

class CandidateProfile(BaseModel):
    """
    Represents a candidate's profile for expert matching.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="candidate_profiles",
        help_text="User associated with this candidate profile."
    )
    skills = models.JSONField(null=True, blank=True, help_text="JSON data representing skills and expertise.")
    reputation_score = models.FloatField(default=0, help_text="Reputation score from the ekoh system.")

    def __str__(self):
        return f"Candidate Profile for {self.user}"

class MatchScore(BaseModel):
    """
    Represents the compatibility score between a match request and a candidate.
    """
    match_request = models.ForeignKey(
        ExpertMatchRequest,
        on_delete=models.CASCADE,
        related_name="match_scores",
        help_text="The expert match request."
    )
    candidate = models.ForeignKey(
        CandidateProfile,
        on_delete=models.CASCADE,
        related_name="match_scores",
        help_text="Candidate profile being evaluated."
    )
    score = models.FloatField(help_text="Computed compatibility score.")

    def __str__(self):
        return f"Match Score: {self.candidate.user} - {self.score}"
