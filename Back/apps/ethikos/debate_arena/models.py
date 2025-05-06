"""
File: apps/ethikos/debate_arena/models.py

Purpose:
Define models for real‑time debate sessions, including threaded arguments,
vote records, and audit trails.
"""

from django.db import models
from common.base_models import BaseModel

class DebateSession(BaseModel):
    """
    Represents a real-time debate session.
    """
    topic = models.CharField(max_length=255, help_text="Title or topic of the debate session")
    description = models.TextField(null=True, blank=True, help_text="Description of the debate session")
    moderator = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="moderated_debates",
        help_text="Moderator of the debate session"
    )
    start_time = models.DateTimeField(help_text="Debate start time")
    end_time = models.DateTimeField(null=True, blank=True, help_text="Debate end time")
    is_active = models.BooleanField(default=True, help_text="Indicates if the debate session is active")

    def __str__(self):
        return self.topic

class Argument(BaseModel):
    """
    Represents an argument within a debate session.
    Supports threaded replies.
    """
    debate_session = models.ForeignKey(
        DebateSession,
        on_delete=models.CASCADE,
        related_name="arguments",
        help_text="Debate session this argument belongs to"
    )
    author = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="arguments",
        help_text="User who posted the argument"
    )
    content = models.TextField(help_text="Content of the argument")
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Parent argument for threaded discussions"
    )
    vote_count = models.IntegerField(default=0, help_text="Net vote count for the argument")

    def __str__(self):
        return f"Argument by {self.author} in {self.debate_session.topic}"

class VoteRecord(BaseModel):
    """
    Records a vote on an argument within a debate session.
    """
    argument = models.ForeignKey(
        Argument,
        on_delete=models.CASCADE,
        related_name="vote_records",
        help_text="The argument being voted on"
    )
    voter = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="vote_records",
        help_text="User who cast the vote"
    )
    vote_value = models.IntegerField(help_text="Vote value, e.g., +1 or -1")
    timestamp = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the vote was cast")

    def __str__(self):
        return f"Vote by {self.voter} on Argument {self.argument.id}: {self.vote_value}"
