from rest_framework import serializers
from ethikos.debate_arena.models import DebateSession, Argument, VoteRecord

class DebateSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DebateSession
        fields = [
            'id',
            'topic',
            'description',
            'moderator',
            'start_time',
            'end_time',
            'is_active',
            'created_at',
            'updated_at'
        ]

class ArgumentSerializer(serializers.ModelSerializer):
    # Recursively include replies
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Argument
        fields = [
            'id',
            'debate_session',
            'author',
            'content',
            'parent',
            'vote_count',
            'created_at',
            'updated_at',
            'replies'
        ]

    def get_replies(self, obj):
        qs = obj.replies.all()
        return ArgumentSerializer(qs, many=True).data

class VoteRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VoteRecord
        fields = [
            'id',
            'argument',
            'voter',
            'vote_value',
            'timestamp',
            'created_at',
            'updated_at'
        ]
