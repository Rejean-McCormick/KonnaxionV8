from rest_framework import serializers
from konnected.paths.models import LearningPath, PathStep

class LearningPathSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPath
        fields = [
            'id',
            'title',
            'description',
            'created_by',
            'created_at',
            'updated_at'
        ]

class PathStepSerializer(serializers.ModelSerializer):
    learning_path = serializers.PrimaryKeyRelatedField(read_only=True)
    knowledge_unit = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PathStep
        fields = [
            'id',
            'learning_path',
            'knowledge_unit',
            'order',
            'created_at',
            'updated_at'
        ]
