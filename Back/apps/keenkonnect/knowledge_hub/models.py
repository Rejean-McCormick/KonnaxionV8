"""
File: apps/keenkonnect/keenKnowledgeHub/models.py

This module defines models for a repository of blueprints, research documents,
and version-controlled designs.
"""

from django.db import models
from common.base_models import BaseModel

class KnowledgeDocument(BaseModel):
    """
    Represents a document such as a blueprint or research paper.
    """
    title = models.CharField(max_length=255, help_text="Title of the document.")
    description = models.TextField(null=True, blank=True, help_text="Description of the document.")
    document_file = models.FileField(upload_to="knowledge_documents/", help_text="Uploaded document file.")
    version = models.CharField(max_length=50, default="1.0", help_text="Document version.")
    created_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="knowledge_documents",
        help_text="User who created/uploaded the document."
    )

    def __str__(self):
        return f"{self.title} (v{self.version})"

class DocumentRevision(BaseModel):
    """
    Represents a revision of a knowledge document.
    """
    knowledge_document = models.ForeignKey(
        KnowledgeDocument,
        on_delete=models.CASCADE,
        related_name="revisions",
        help_text="The document to which this revision belongs."
    )
    revision_number = models.CharField(max_length=50, help_text="Revision number or identifier.")
    changes = models.TextField(help_text="Description of the changes in this revision.")
    revised_by = models.ForeignKey(
        "core.CustomUser",
        on_delete=models.SET_NULL,
        null=True,
        related_name="document_revisions",
        help_text="User who made the revision."
    )
    revised_at = models.DateTimeField(auto_now_add=True, help_text="Timestamp when the revision was made.")

    def __str__(self):
        return f"{self.knowledge_document.title} Revision {self.revision_number}"
