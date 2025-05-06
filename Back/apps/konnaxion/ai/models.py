"""
File: apps/konnaxion/ai/models.py

This module defines models for AI/ML functionalities that enhance content,
provide recommendations, and perform sentiment analysis.
"""

from django.db import models
from common.base_models import BaseModel

class AIResult(BaseModel):
    """
    Model to store AI-generated results, such as content summaries,
    translations, recommendations, and sentiment analysis.
    """
    RESULT_TYPE_CHOICES = [
        ('summary', 'Summary'),
        ('translation', 'Translation'),
        ('recommendation', 'Recommendation'),
        ('sentiment', 'Sentiment Analysis'),
    ]
    result_type = models.CharField(
        max_length=20,
        choices=RESULT_TYPE_CHOICES,
        help_text="Type of AI result."
    )
    result_data = models.JSONField(
        help_text="The AI-generated result data in JSON format."
    )
    source_model = models.CharField(
        max_length=100,
        help_text="Name of the source model (e.g., Lesson, Debate)."
    )
    source_object_id = models.PositiveIntegerField(
        help_text="ID of the source object for which the AI result was generated."
    )

    def __str__(self):
        return f"{self.get_result_type_display()} for {self.source_model} #{self.source_object_id}"
