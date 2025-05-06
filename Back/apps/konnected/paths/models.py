"""
File: apps/konnected/paths/models.py

This module enables the creation of adaptive learning paths.
It includes models for assembling knowledge units into personalized curricula.
"""

from django.db import models
from common.base_models import BaseModel

class LearningPath(BaseModel):
    """
    Represents a personalized learning path (curriculum).
    """
    title = models.CharField(max_length=255, help_text="Title of the learning path.")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the learning path."
    )
    created_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="User who created the learning path."
    )

    def __str__(self):
        return self.title

class PathStep(BaseModel):
    """
    Represents an individual step within a learning path, linking a knowledge unit.
    """
    learning_path = models.ForeignKey(
        LearningPath,
        on_delete=models.CASCADE,
        related_name="steps",
        help_text="The learning path this step belongs to."
    )
    knowledge_unit = models.ForeignKey(
        "foundation.KnowledgeUnit",
        on_delete=models.CASCADE,
        related_name="path_steps",
        help_text="The knowledge unit associated with this step."
    )
    order = models.PositiveIntegerField(help_text="The order/sequence of this step in the learning path.")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.learning_path.title} - Step {self.order}: {self.knowledge_unit.title}"
