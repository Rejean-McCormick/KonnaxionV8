from rest_framework import serializers
from konnaxion.notifications.models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    recipient = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Notification
        fields = [
            'id',
            'sender',
            'recipient',
            'message',
            'notification_type',
            'is_read',
            'created_at',
            'updated_at'
        ]
