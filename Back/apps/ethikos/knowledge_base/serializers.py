from rest_framework import serializers
from ethikos.knowledge_base.models import DebateArchive

class DebateArchiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateArchive
        fields = [
            'id',
            'title',
            'content',
            'debate_date',
            'source',
            'tags',
            'created_at',
            'updated_at'
        ]
