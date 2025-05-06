"""
File: apps/konnected/team/models.py

This module facilitates team creation and management for educational projects.
It includes models for teams and team invitations.
"""

from django.db import models
from common.base_models import BaseModel

class Team(BaseModel):
    """
    Represents an educational team.
    """
    name = models.CharField(max_length=255, help_text="Name of the team.")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the team."
    )
    members = models.ManyToManyField(
        "core.CustomUser",
        related_name="teams",
        help_text="Users who are members of this team."
    )

    def __str__(self):
        return self.name

class TeamInvitation(BaseModel):
    """
    Represents an invitation for a user to join a team.
    """
    INVITATION_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name="invitations",
        help_text="Team for which the invitation is sent."
    )
    invited_user = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.CASCADE,
        related_name="team_invitations",
        help_text="User who is invited."
    )
    status = models.CharField(
        max_length=20,
        choices=INVITATION_STATUS_CHOICES,
        default="pending",
        help_text="Status of the invitation."
    )
    message = models.TextField(
        null=True,
        blank=True,
        help_text="Optional message accompanying the invitation."
    )

    def __str__(self):
        return f"Invitation for {self.invited_user} to join {self.team.name} [{self.status}]"
