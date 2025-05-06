from rest_framework import serializers
from konnaxion.core.models import CustomUser, SystemConfiguration, ConfigurationChangeLog

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'language_preference',
            'device_details',
            'role',
            'offline_sync_token',
            'created_at',
            'updated_at'
        ]

class SystemConfigurationSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemConfiguration
        fields = [
            'id',
            'key',
            'value',
            'description',
            'created_at',
            'updated_at'
        ]

class ConfigurationChangeLogSerializer(serializers.ModelSerializer):
    configuration = serializers.PrimaryKeyRelatedField(read_only=True)
    changed_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ConfigurationChangeLog
        fields = [
            'id',
            'configuration',
            'old_value',
            'new_value',
            'changed_by',
            'change_reason',
            'created_at',
            'updated_at'
        ]
