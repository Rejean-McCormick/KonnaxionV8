"""
File: apps/konnaxion/ekoh/models.py

Purpose:
Develop the reputation and ethical trust engine models, including detailed reputation
profiles, event logs, weighted voting, and expertise tags.
"""

from django.db import models
from common.base_models import BaseModel

class ExpertiseTag(BaseModel):
    """
    Represents an expertise tag that classifies a user's area of specialization.
    """
    name = models.CharField(max_length=100, unique=True, help_text="Name of the expertise tag")
    description = models.TextField(null=True, blank=True, help_text="Description of the expertise tag")

    def __str__(self):
        return self.name

class ReputationProfile(BaseModel):
    """
    Captures detailed reputation and ethical trust data for a user.
    """
    user = models.OneToOneField(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="reputation_profile",
        help_text="User's reputation profile"
    )
    reputation_score = models.FloatField(default=0, help_text="Overall reputation score")
    ethical_multiplier = models.FloatField(default=1.0, help_text="Multiplier used for ethical adjustments")
    expertise_tags = models.ManyToManyField(
        ExpertiseTag,
        blank=True,
        related_name="profiles",
        help_text="Expertise tags assigned to the user"
    )

    def __str__(self):
        return f"Reputation Profile for {self.user}"

class ReputationEvent(BaseModel):
    """
    Logs events that impact a user's reputation.
    """
    reputation_profile = models.ForeignKey(
        ReputationProfile,
        on_delete=models.CASCADE,
        related_name="events",
        help_text="Associated reputation profile"
    )
    event_type = models.CharField(max_length=50, help_text="Type of event (e.g., vote, contribution)")
    event_value = models.FloatField(help_text="Numerical impact of the event")
    description = models.TextField(null=True, blank=True, help_text="Context or description of the event")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="When the event occurred")

    def __str__(self):
        return f"{self.event_type} event for {self.reputation_profile.user}"

class WeightedVote(BaseModel):
    """
    Records a vote cast by a user with a weight determined by reputation.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="weighted_votes",
        help_text="User casting the vote"
    )
    target_id = models.PositiveIntegerField(help_text="ID of the target (e.g., a debate argument)")
    vote_value = models.IntegerField(help_text="Vote value (e.g., +1 or -1)")
    weight = models.FloatField(help_text="Vote weight based on reputation")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the vote was cast")

    def __str__(self):
        return f"Vote by {self.user} on target {self.target_id}: {self.vote_value}"
