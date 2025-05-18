# apps/ethikos/home/serializers.py

from rest_framework import serializers
from ethikos.home.models import (
    DebateCategory,
    ResponseFormat,
    DebateTopic,
    FeaturedDebate,
    PersonalizedRecommendation,
    PublicVote,
)

class DebateCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateCategory
        fields = ["id", "name"]


class ResponseFormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResponseFormat
        fields = ["id", "name", "code"]


class DebateTopicSerializer(serializers.ModelSerializer):
    turnout = serializers.IntegerField(read_only=True)

    class Meta:
        model = DebateTopic
        fields = [
            "id",
            "question",
            "description",
            "debatecategory",
            "responseformat",
            "options",
            "scale_labels",
            "turnout",
            "created_at",
            "updated_at",
        ]


class FeaturedDebateSerializer(serializers.ModelSerializer):
    debate_topic = DebateTopicSerializer(read_only=True)

    class Meta:
        model = FeaturedDebate
        fields = [
            "id",
            "debate_topic",
            "display_order",
            "active",
            "created_at",
            "updated_at",
        ]


class PersonalizedRecommendationSerializer(serializers.ModelSerializer):
    debate_topic = DebateTopicSerializer(read_only=True)

    class Meta:
        model = PersonalizedRecommendation
        fields = [
            "id",
            "user",
            "debate_topic",
            "score",
            "created_at",
            "updated_at",
        ]


class PublicVoteSerializer(serializers.ModelSerializer):
    topic = serializers.PrimaryKeyRelatedField(
        queryset=DebateTopic.objects.filter(is_active=True, is_deleted=False)
    )

    class Meta:
        model = PublicVote
        fields = ["id", "topic", "value", "created_at"]
        read_only_fields = ["id", "created_at"]
