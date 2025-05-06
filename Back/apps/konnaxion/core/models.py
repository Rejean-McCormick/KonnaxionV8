"""
File: apps/konnaxion/core/models.py

This module defines the core models for user management and system configuration.
It includes a custom user model (extending Django’s AbstractUser) and models for
system-wide settings and configuration change logging.
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from common.base_models import BaseModel

class CustomUser(BaseModel, AbstractUser):
    """
    Custom user model with additional fields for roles, language preferences,
    device details, and offline synchronization metadata.
    """
    language_preference = models.CharField(
        max_length=10,
        default="en",
        help_text="User's preferred language code."
    )
    device_details = models.JSONField(
        null=True, blank=True,
        help_text="JSON field storing device-related information."
    )
    role = models.CharField(
        max_length=50,
        default="user",
        help_text="User role (e.g., user, admin, moderator)."
    )
    offline_sync_token = models.CharField(
        max_length=255,
        null=True, blank=True,
        help_text="Token for offline synchronization."
    )

    def __str__(self):
        return self.username


class SystemConfiguration(BaseModel):
    """
    Model for storing system-wide configuration settings.
    """
    key = models.CharField(
        max_length=100,
        unique=True,
        help_text="Configuration key identifier."
    )
    value = models.TextField(
        help_text="Configuration value stored as text (JSON or plain text)."
    )
    description = models.TextField(
        null=True, blank=True,
        help_text="Optional description of the configuration setting."
    )

    def __str__(self):
        return f"{self.key}: {self.value}"


class ConfigurationChangeLog(BaseModel):
    """
    Model to log configuration changes for auditing purposes.
    """
    configuration = models.ForeignKey(
        SystemConfiguration,
        on_delete=models.CASCADE,
        related_name="change_logs"
    )
    old_value = models.TextField(
        help_text="Previous configuration value."
    )
    new_value = models.TextField(
        help_text="New configuration value."
    )
    changed_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True, blank=True,
        help_text="User who made the change."
    )
    change_reason = models.TextField(
        null=True, blank=True,
        help_text="Optional reason for the change."
    )

    def __str__(self):
        return f"Change on {self.configuration.key} by {self.changed_by or 'System'}"
