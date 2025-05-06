"""
File: apps/konnaxion/messaging/models.py

This module defines models for real‑time and persistent messaging, including
conversation threads and individual messages.
"""

from django.db import models
from common.base_models import BaseModel

class Conversation(BaseModel):
    """
    Model representing a conversation or chat thread between users.
    """
    participants = models.ManyToManyField(
        "core.CustomUser",
        related_name='conversations',
        help_text="Users participating in this conversation."
    )
    title = models.CharField(
        max_length=255,
        null=True, blank=True,
        help_text="Optional title for the conversation."
    )

    def __str__(self):
        # Note: accessing all participants in __str__ might be heavy in some contexts.
        participant_names = ", ".join([str(user) for user in self.participants.all()])
        return f"Conversation between: {participant_names}"


class Message(BaseModel):
    """
    Model for individual messages within a conversation.
    """
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
        help_text="The conversation this message belongs to."
    )
    sender = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name='sent_messages',
        help_text="User who sent the message."
    )
    content = models.TextField(
        help_text="The text content of the message."
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Indicates if the message has been read by the recipient."
    )

    def __str__(self):
        return f"Message from {self.sender} in Conversation #{self.conversation.id}"
