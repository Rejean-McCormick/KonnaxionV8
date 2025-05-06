from rest_framework import serializers
from keenkonnect.collab_spaces.models import CollabSpace, Document, ChatMessage

class CollabSpaceSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = CollabSpace
        fields = [
            'id',
            'name',
            'description',
            'created_by',
            'participants',
            'is_active',
            'created_at',
            'updated_at'
        ]

class DocumentSerializer(serializers.ModelSerializer):
    collab_space = serializers.PrimaryKeyRelatedField(read_only=True)
    uploaded_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Document
        fields = [
            'id',
            'collab_space',
            'title',
            'file',
            'description',
            'uploaded_by',
            'uploaded_at',
            'created_at',
            'updated_at'
        ]

class ChatMessageSerializer(serializers.ModelSerializer):
    collab_space = serializers.PrimaryKeyRelatedField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            'id',
            'collab_space',
            'sender',
            'message',
            'created_at',
            'updated_at'
        ]
