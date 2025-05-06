from rest_framework import serializers
from keenkonnect.projects.models import Project, Milestone, Task

class ProjectSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Project
        fields = [
            'id',
            'title',
            'description',
            'owner',
            'progress',
            'start_date',
            'end_date',
            'status',
            'created_at',
            'updated_at'
        ]

class MilestoneSerializer(serializers.ModelSerializer):
    project = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Milestone
        fields = [
            'id',
            'project',
            'title',
            'description',
            'due_date',
            'status',
            'created_at',
            'updated_at'
        ]

class TaskSerializer(serializers.ModelSerializer):
    milestone = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'id',
            'milestone',
            'title',
            'description',
            'assigned_to',
            'due_date',
            'is_completed',
            'created_at',
            'updated_at'
        ]
