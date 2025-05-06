from rest_framework import serializers
from konnaxion.ai.models import AIResult

class AIResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIResult
        fields = [
            'id',
            'result_type',
            'result_data',
            'source_model',
            'source_object_id',
            'created_at',
            'updated_at'
        ]
