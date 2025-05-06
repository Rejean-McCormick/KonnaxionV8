from rest_framework import serializers
from keenkonnect.knowledge_hub.models import KnowledgeDocument, DocumentRevision

class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDocument
        fields = [
            'id',
            'title',
            'description',
            'document_file',
            'version',
            'created_by',
            'created_at',
            'updated_at'
        ]

class DocumentRevisionSerializer(serializers.ModelSerializer):
    knowledge_document = serializers.PrimaryKeyRelatedField(read_only=True)
    revised_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DocumentRevision
        fields = [
            'id',
            'knowledge_document',
            'revision_number',
            'changes',
            'revised_by',
            'revised_at',
            'created_at',
            'updated_at'
        ]
