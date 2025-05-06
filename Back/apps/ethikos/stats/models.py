"""
File: apps/ethikos/ethikos_stats/models.py

This module builds models to capture statistical data for debates.
It supports time‑series analytics and logs events for dashboard displays.
"""

from django.db import models
from common.base_models import BaseModel

class DebateStatistic(BaseModel):
    """
    Represents a time-series statistical record for a debate session.
    """
    debate_session = models.ForeignKey(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="statistics",
        help_text="Associated debate session"
    )
    metric_name = models.CharField(max_length=100, help_text="Name of the metric (e.g., total_votes, active_participants)")
    value = models.FloatField(help_text="Recorded value of the metric")
    recorded_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the metric was recorded")

    def __str__(self):
        return f"{self.metric_name} for {self.debate_session.topic}: {self.value}"

class DebateEventLog(BaseModel):
    """
    Logs events related to debates for analytics and audit purposes.
    """
    debate_session = models.ForeignKey(
        "debate_arena.DebateSession",
        on_delete=models.CASCADE,
        related_name="event_logs",
        help_text="Debate session associated with this event"
    )
    event_type = models.CharField(max_length=100, help_text="Type of event (e.g., 'argument_posted', 'vote_cast')")
    description = models.TextField(null=True, blank=True, help_text="Detailed description of the event")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp of the event")

    def __str__(self):
        return f"Event {self.event_type} at {self.timestamp}"
