from rest_framework import serializers
from kreative.kreativecommunity.models import CommunityPost, PostComment, ArtworkReview

class CommunityPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityPost
        fields = [
            'id',
            'title',
            'content',
            'posted_by',
            'created_at',
            'updated_at'
        ]

class PostCommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = PostComment
        fields = [
            'id',
            'post',
            'parent',
            'content',
            'commented_by',
            'created_at',
            'updated_at',
            'replies'
        ]

    def get_replies(self, obj):
        qs = obj.replies.all()
        return PostCommentSerializer(qs, many=True).data

class ArtworkReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ArtworkReview
        fields = [
            'id',
            'artwork',
            'reviewed_by',
            'rating',
            'review_text',
            'created_at',
            'updated_at'
        ]
