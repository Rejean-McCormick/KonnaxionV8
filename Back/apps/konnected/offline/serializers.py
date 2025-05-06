from rest_framework import serializers
from konnected.offline.models import OfflineContentPackage

class OfflineContentPackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfflineContentPackage
        fields = [
            'id',
            'title',
            'description',
            'content_data',
            'last_synced',
            'conflict_resolution_notes',
            'created_at',
            'updated_at'
        ]
