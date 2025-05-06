from rest_framework import serializers
from keenkonnect.team_formation.models import TeamFormationRequest, TeamFormationCandidate

class TeamFormationRequestSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    requested_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TeamFormationRequest
        fields = [
            'id',
            'project',
            'requested_by',
            'required_roles',
            'additional_info',
            'created_at',
            'updated_at'
        ]

class TeamFormationCandidateSerializer(serializers.ModelSerializer):
    formation_request = serializers.PrimaryKeyRelatedField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TeamFormationCandidate
        fields = [
            'id',
            'formation_request',
            'user',
            'skills',
            'compatibility_score',
            'created_at',
            'updated_at'
        ]
