from rest_framework import serializers
from konnaxion.messaging.models import Conversation, Message

class ConversationSerializer(serializers.ModelSerializer):
    participants = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'participants',
            'title',
            'created_at',
            'updated_at'
        ]

class MessageSerializer(serializers.ModelSerializer):
    conversation = serializers.PrimaryKeyRelatedField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Message
        fields = [
            'id',
            'conversation',
            'sender',
            'content',
            'is_read',
            'created_at',
            'updated_at'
        ]
