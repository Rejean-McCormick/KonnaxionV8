from rest_framework import serializers
from keenkonnect.gap_analysis.models import GapAnalysis

class GapAnalysisSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = GapAnalysis
        fields = [
            'id',
            'project',
            'planned_progress',
            'actual_progress',
            'gap',
            'recommendations',
            'created_at',
            'updated_at'
        ]
