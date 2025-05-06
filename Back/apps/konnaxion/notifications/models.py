"""
File: apps/konnaxion/notifications/models.py

This module defines the Notification model, which centralizes the creation and
delivery of notifications across the platform.
"""

from django.db import models
from common.base_models import BaseModel

class Notification(BaseModel):
    """
    Model for system notifications.
    """
    NOTIFICATION_TYPE_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
    ]
    sender = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sent_notifications',
        help_text="User who triggered the notification."
    )
    recipient = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name='notifications',
        help_text="User who receives the notification."
    )
    message = models.TextField(
        help_text="Notification message content."
    )
    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPE_CHOICES,
        default='info',
        help_text="Type/category of notification."
    )
    is_read = models.BooleanField(
        default=False,
        help_text="Indicates if the notification has been read."
    )

    def __str__(self):
        return f"Notification for {self.recipient} - {self.get_notification_type_display()}"
