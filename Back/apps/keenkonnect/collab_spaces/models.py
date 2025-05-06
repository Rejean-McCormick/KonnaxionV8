"""
File: \apps\keenkonnect\collab_spaces/models.py

This module defines models for real-time collaboration spaces.
It includes models for collaborative workspaces, document sharing, and chat messages.
"""

from django.db import models
from common.base_models import BaseModel

class CollabSpace(BaseModel):
    """
    Represents a collaborative workspace.
    """
    name = models.CharField(max_length=255, help_text="Name of the collaboration space.")
    description = models.TextField(null=True, blank=True, help_text="Description of the space.")
    created_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="collab_spaces_created",
        help_text="User who created the space."
    )
    participants = models.ManyToManyField(
        "core.CustomUser",
        related_name="collab_spaces",
        help_text="Users participating in the space."
    )
    is_active = models.BooleanField(default=True, help_text="Indicates if the space is active.")

    def __str__(self):
        return self.name

class Document(BaseModel):
    """
    Represents a document shared within a collaboration space.
    """
    collab_space = models.ForeignKey(
        CollabSpace,
        on_delete=models.CASCADE,
        related_name="documents",
        help_text="Collaboration space where the document is shared."
    )
    title = models.CharField(max_length=255, help_text="Title of the document.")
    file = models.FileField(upload_to="collab_documents/", help_text="Uploaded file for the document.")
    description = models.TextField(null=True, blank=True, help_text="Optional description.")
    uploaded_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="uploaded_documents",
        help_text="User who uploaded the document."
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, help_text="Upload timestamp.")

    def __str__(self):
        return self.title

class ChatMessage(BaseModel):
    """
    Represents a chat message within a collaboration space.
    """
    collab_space = models.ForeignKey(
        CollabSpace,
        on_delete=models.CASCADE,
        related_name="chat_messages",
        help_text="Collaboration space where the message was sent."
    )
    sender = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="chat_messages",
        help_text="User who sent the message."
    )
    message = models.TextField(help_text="Content of the chat message.")
    is_read = models.BooleanField(default=False, help_text="Indicates if the message has been read.")

    def __str__(self):
        return f"Message from {self.sender} in {self.collab_space.name}"
