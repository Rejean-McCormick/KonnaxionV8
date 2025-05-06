"""
File: apps/kreative/kreative_immersive/models.py

Purpose:
(Optional/Future) Define minimal placeholder models to support AR/VR and immersive cultural experiences.
"""

from django.db import models
from common.base_models import BaseModel

class ImmersiveExperience(BaseModel):
    """
    Placeholder model for AR/VR and immersive cultural experiences.
    """
    title = models.CharField(max_length=255, help_text="Title of the immersive experience")
    description = models.TextField(help_text="Description of the immersive experience")
    media_url = models.URLField(null=True, blank=True, help_text="URL for the immersive AR/VR content")

    def __str__(self):
        return self.title
