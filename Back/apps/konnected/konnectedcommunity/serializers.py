from rest_framework import serializers
from konnected.konnectedcommunity.models import DiscussionThread, Comment

class DiscussionThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscussionThread
        fields = [
            'id',
            'title',
            'content',
            'author',
            'created_at',
            'updated_at'
        ]

class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'thread',
            'parent',
            'author',
            'content',
            'vote_count',
            'created_at',
            'updated_at',
            'replies'
        ]

    def get_replies(self, obj):
        qs = obj.replies.all()
        return CommentSerializer(qs, many=True).data
