from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    """
    A base serializer that provides common configuration.
    Extend this serializer in your app-specific serializers to inherit shared settings.
    """
    class Meta:
        abstract = True

class TimestampedSerializer(BaseSerializer):
    """
    A mixin serializer that automatically includes read-only created_at and updated_at fields.
    Assumes that the model has these fields.
    """
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
