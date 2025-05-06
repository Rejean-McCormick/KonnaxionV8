"""
File: apps/konnaxion/search/models.py

This module defines models related to search functionality. It includes models
for managing search index configurations and logging user search queries.
"""

from django.db import models
from common.base_models import BaseModel

class SearchIndex(BaseModel):
    """
    Model for storing search index configurations.
    """
    name = models.CharField(
        max_length=255,
        help_text="Name of the search index."
    )
    settings = models.JSONField(
        null=True, blank=True,
        help_text="JSON configuration for the index."
    )
    last_updated = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the index was last updated."
    )

    def __str__(self):
        return self.name


class SearchQueryLog(BaseModel):
    """
    Model for logging search queries performed by users.
    """
    user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="User who made the search query."
    )
    query_text = models.TextField(
        help_text="The search query entered by the user."
    )
    results_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of results returned for the query."
    )

    def __str__(self):
        return f"Query: {self.query_text[:50]}"
