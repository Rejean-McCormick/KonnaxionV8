from rest_framework import serializers
from konnaxion.ekoh.models import ExpertiseTag, ReputationProfile, ReputationEvent, WeightedVote

class ExpertiseTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertiseTag
        fields = [
            'id',
            'name',
            'description',
            'created_at',
            'updated_at'
        ]

class ReputationProfileSerializer(serializers.ModelSerializer):
    expertise_tags = ExpertiseTagSerializer(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReputationProfile
        fields = [
            'id',
            'user',
            'reputation_score',
            'ethical_multiplier',
            'expertise_tags',
            'created_at',
            'updated_at'
        ]

class ReputationEventSerializer(serializers.ModelSerializer):
    reputation_profile = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ReputationEvent
        fields = [
            'id',
            'reputation_profile',
            'event_type',
            'event_value',
            'description',
            'timestamp',
            'created_at',
            'updated_at'
        ]

class WeightedVoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = WeightedVote
        fields = [
            'id',
            'user',
            'target_id',
            'vote_value',
            'weight',
            'timestamp',
            'created_at',
            'updated_at'
        ]
