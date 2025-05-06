from rest_framework import serializers
from keenkonnect.expert_match.models import ExpertMatchRequest, CandidateProfile, MatchScore

class ExpertMatchRequestSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)
    requested_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ExpertMatchRequest
        fields = [
            'id',
            'project',
            'requested_by',
            'description',
            'criteria',
            'created_at',
            'updated_at'
        ]

class CandidateProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CandidateProfile
        fields = [
            'id',
            'user',
            'skills',
            'reputation_score',
            'created_at',
            'updated_at'
        ]

class MatchScoreSerializer(serializers.ModelSerializer):
    match_request = serializers.PrimaryKeyRelatedField(read_only=True)
    candidate = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = MatchScore
        fields = [
            'id',
            'match_request',
            'candidate',
            'score',
            'created_at',
            'updated_at'
        ]
