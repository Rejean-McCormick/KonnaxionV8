"""
File: apps/keenkonnectgap_analysis/models.py

This module defines models to record gap analysis data for projects.
It compares planned versus actual progress and stores recommendations.
"""

from django.db import models
from common.base_models import BaseModel

class GapAnalysis(BaseModel):
    """
    Represents a gap analysis record for a project.
    """
    project = models.ForeignKey(
        "projects.Project",
        on_delete=models.CASCADE,
        related_name="gap_analyses",
        help_text="Project for which the gap analysis is performed."
    )
    planned_progress = models.PositiveIntegerField(help_text="Planned progress percentage.")
    actual_progress = models.PositiveIntegerField(help_text="Actual progress percentage.")
    gap = models.PositiveIntegerField(help_text="Difference between planned and actual progress.")
    recommendations = models.TextField(null=True, blank=True, help_text="Recommendations to close the gap.")

    def __str__(self):
        return f"Gap Analysis for {self.project.title}"
