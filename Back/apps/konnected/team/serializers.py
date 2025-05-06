from rest_framework import serializers
from konnected.team.models import Team, TeamInvitation

class TeamSerializer(serializers.ModelSerializer):
    members = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Team
        fields = [
            'id',
            'name',
            'description',
            'members',
            'created_at',
            'updated_at'
        ]

class TeamInvitationSerializer(serializers.ModelSerializer):
    team = serializers.PrimaryKeyRelatedField(read_only=True)
    invited_user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = TeamInvitation
        fields = [
            'id',
            'team',
            'invited_user',
            'status',
            'message',
            'created_at',
            'updated_at'
        ]
