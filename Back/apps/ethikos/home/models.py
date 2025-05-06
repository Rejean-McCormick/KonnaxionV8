"""
File: apps/ethikos/ethikos_home/models.py

Purpose:
Create models for the debate landing portal, storing debate topics, featured items,
and personalized recommendations.
"""

from django.db import models
from common.base_models import BaseModel

class DebateTopic(BaseModel):
    """
    Represents a debate topic or category.
    """
    title = models.CharField(max_length=255, help_text="Title of the debate topic")
    description = models.TextField(help_text="Description of the debate topic")
    is_active = models.BooleanField(default=True, help_text="Whether the debate topic is active")
    publish_date = models.DateTimeField(null=True, blank=True, help_text="Publish date of the topic")

    def __str__(self):
        return self.title

class FeaturedDebate(BaseModel):
    """
    Marks a debate topic as featured on the landing portal.
    """
    debate_topic = models.ForeignKey(
        DebateTopic,
        on_delete=models.CASCADE,
        related_name="featured_entries",
        help_text="Featured debate topic"
    )
    display_order = models.PositiveIntegerField(default=0, help_text="Order for display")
    active = models.BooleanField(default=True, help_text="Whether this featured entry is active")

    def __str__(self):
        return f"Featured: {self.debate_topic.title}"

class PersonalizedRecommendation(BaseModel):
    """
    Stores personalized debate topic recommendations for users.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="User receiving the recommendation"
    )
    debate_topic = models.ForeignKey(
        DebateTopic,
        on_delete=models.CASCADE,
        related_name="recommendations",
        help_text="Recommended debate topic"
    )
    score = models.FloatField(default=0, help_text="Relevance score for the recommendation")

    def __str__(self):
        return f"Recommendation for {self.user}: {self.debate_topic.title}"
