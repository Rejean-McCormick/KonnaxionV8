"""
File: apps/ethikos/ethikos_knowledge_base/models.py

This module creates archival models for debates, philosophical texts,
and legal precedents. It supports full‑text search and filtering.
"""

from django.db import models
from common.base_models import BaseModel

class DebateArchive(BaseModel):
    """
    Archives debates and related texts for historical and research purposes.
    """
    title = models.CharField(max_length=255, help_text="Title of the archived debate or text")
    content = models.TextField(help_text="Full text content for search and analysis")
    debate_date = models.DateField(null=True, blank=True, help_text="Date of the debate or publication")
    source = models.CharField(max_length=255, null=True, blank=True, help_text="Source or reference of the material")
    tags = models.JSONField(null=True, blank=True, help_text="List of tags for filtering and search")

    def __str__(self):
        return self.title
