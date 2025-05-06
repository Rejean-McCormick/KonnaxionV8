# apps/keenkonnect/knowledge_hub/admin.py

from django.contrib import admin
from keenkonnect.knowledge_hub.models import KnowledgeDocument, DocumentRevision

class DocumentRevisionInline(admin.TabularInline):
    model = DocumentRevision
    extra = 0
    fields = ('revision_number', 'changes', 'revised_by', 'revised_at')
    readonly_fields = ('revised_at',)

@admin.register(KnowledgeDocument)
class KnowledgeDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'version', 'created_by', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('title',)
    inlines = [DocumentRevisionInline]

@admin.register(DocumentRevision)
class DocumentRevisionAdmin(admin.ModelAdmin):
    list_display = ('knowledge_document', 'revision_number', 'revised_by', 'revised_at')
    list_filter = ('knowledge_document',)
    search_fields = ('knowledge_document__title',)
    ordering = ('-revised_at',)
