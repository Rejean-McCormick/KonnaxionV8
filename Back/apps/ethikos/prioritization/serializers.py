from rest_framework import serializers
from ethikos.prioritization.models import DebatePrioritization

class DebatePrioritizationSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebatePrioritization
        fields = [
            'id',
            'debate_session',
            'ranking_score',
            'criteria',
            'notes',
            'created_at',
            'updated_at'
        ]
