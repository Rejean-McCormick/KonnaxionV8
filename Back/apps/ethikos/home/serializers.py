from rest_framework import serializers
from ethikos.home.models import DebateTopic, FeaturedDebate, PersonalizedRecommendation

class DebateTopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateTopic
        fields = [
            'id',
            'title',
            'description',
            'is_active',
            'publish_date',
            'created_at',
            'updated_at'
        ]

class FeaturedDebateSerializer(serializers.ModelSerializer):
    debate_topic = DebateTopicSerializer(read_only=True)

    class Meta:
        model = FeaturedDebate
        fields = [
            'id',
            'debate_topic',
            'display_order',
            'active',
            'created_at',
            'updated_at'
        ]

class PersonalizedRecommendationSerializer(serializers.ModelSerializer):
    debate_topic = DebateTopicSerializer(read_only=True)

    class Meta:
        model = PersonalizedRecommendation
        fields = [
            'id',
            'user',
            'debate_topic',
            'score',
            'created_at',
            'updated_at'
        ]
