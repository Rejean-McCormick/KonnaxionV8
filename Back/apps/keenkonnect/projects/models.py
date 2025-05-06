"""
File: apps/keenkonnectprojects/models.py

This module manages the project lifecycle. It includes models for Projects,
Milestones, and Tasks for project collaboration and progress tracking.
"""

from django.db import models
from common.base_models import BaseModel

class Project(BaseModel):
    """
    Represents a collaborative project.
    """
    title = models.CharField(max_length=255, help_text="Title of the project.")
    description = models.TextField(help_text="Detailed description of the project.")
    owner = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="owned_projects",
        help_text="User who created/owns the project."
    )
    progress = models.PositiveIntegerField(default=0, help_text="Progress percentage (0-100) of the project.")
    start_date = models.DateField(null=True, blank=True, help_text="Project start date.")
    end_date = models.DateField(null=True, blank=True, help_text="Project expected end date.")
    status = models.CharField(max_length=50, default="planning", help_text="Current status of the project.")

    def __str__(self):
        return self.title

class Milestone(BaseModel):
    """
    Represents a milestone within a project.
    """
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name="milestones",
        help_text="The project to which this milestone belongs."
    )
    title = models.CharField(max_length=255, help_text="Title of the milestone.")
    description = models.TextField(null=True, blank=True, help_text="Milestone description.")
    due_date = models.DateField(null=True, blank=True, help_text="Due date for the milestone.")
    status = models.CharField(max_length=50, default="pending", help_text="Status of the milestone.")

    def __str__(self):
        return f"{self.project.title} - {self.title}"

class Task(BaseModel):
    """
    Represents a task under a milestone.
    """
    milestone = models.ForeignKey(
        Milestone,
        on_delete=models.CASCADE,
        related_name="tasks",
        help_text="Milestone to which this task belongs."
    )
    title = models.CharField(max_length=255, help_text="Task title.")
    description = models.TextField(null=True, blank=True, help_text="Task description.")
    assigned_to = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="tasks",
        help_text="User assigned to this task."
    )
    due_date = models.DateField(null=True, blank=True, help_text="Due date for the task.")
    is_completed = models.BooleanField(default=False, help_text="Indicates if the task is completed.")

    def __str__(self):
        status = "Completed" if self.is_completed else "Pending"
        return f"{self.title} ({status})"
