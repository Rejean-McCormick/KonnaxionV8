from rest_framework import serializers
from ethikos.stats.models import DebateStatistic, DebateEventLog

class DebateStatisticSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebateStatistic
        fields = [
            'id',
            'debate_session',
            'metric_name',
            'value',
            'recorded_at',
            'created_at',
            'updated_at'
        ]

class DebateEventLogSerializer(serializers.ModelSerializer):
    debate_session = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = DebateEventLog
        fields = [
            'id',
            'debate_session',
            'event_type',
            'description',
            'timestamp',
            'created_at',
            'updated_at'
        ]
