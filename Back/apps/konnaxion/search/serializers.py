from rest_framework import serializers
from konnaxion.search.models import SearchIndex, SearchQueryLog

class SearchIndexSerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchIndex
        fields = [
            'id',
            'name',
            'settings',
            'last_updated',
            'created_at',
            'updated_at'
        ]

class SearchQueryLogSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = SearchQueryLog
        fields = [
            'id',
            'user',
            'query_text',
            'results_count',
            'created_at',
            'updated_at'
        ]
