from rest_framework import serializers
from kreative.immersive.models import ImmersiveExperience

class ImmersiveExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImmersiveExperience
        fields = [
            'id',
            'title',
            'description',
            'media_url',
            'created_at',
            'updated_at'
        ]
