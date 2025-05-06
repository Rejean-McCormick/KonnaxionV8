from rest_framework import serializers
from ethikos.resolution.models import DebateResolution

class DebateResolutionSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)
    approved_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebateResolution
        fields = [
            'id',
            'debate_session',
            'resolution_text',
            'decision_history',
            'approved_by',
            'approved_at',
            'created_at',
            'updated_at'
        ]
