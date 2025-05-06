from rest_framework import serializers
from konnected.foundation.models import KnowledgeUnit

class KnowledgeUnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeUnit
        fields = [
            'id',
            'title',
            'content',
            'attachments',
            'language',
            'version',
            'created_at',
            'updated_at'
        ]
