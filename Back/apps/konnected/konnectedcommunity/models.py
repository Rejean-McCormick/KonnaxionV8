"""
File: apps/konnected/konnectedcommunity/models.py

This module provides a forum for educational Q&A and discussions.
It includes models for discussion threads and nested comments.
"""

from django.db import models
from common.base_models import BaseModel

class DiscussionThread(BaseModel):
    """
    Represents a discussion thread for educational topics.
    """
    title = models.CharField(max_length=255, help_text="Title of the discussion thread.")
    content = models.TextField(help_text="Initial content or description of the thread.")
    author = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="discussion_threads",
        help_text="User who started the discussion."
    )

    def __str__(self):
        return self.title

class Comment(BaseModel):
    """
    Represents a comment on a discussion thread, supporting nested replies.
    """
    thread = models.ForeignKey(
        DiscussionThread,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The discussion thread to which this comment belongs."
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="replies",
        help_text="Parent comment if this is a reply; null if top-level."
    )
    author = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="User who posted the comment."
    )
    content = models.TextField(help_text="Content of the comment.")
    vote_count = models.IntegerField(
        default=0,
        help_text="Net vote count for the comment."
    )

    def __str__(self):
        return f"Comment by {self.author} on {self.thread.title}"
