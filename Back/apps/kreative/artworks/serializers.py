from rest_framework import serializers
from kreative.artworks.models import Exhibition, Artwork

class ExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = [
            'id',
            'name',
            'description',
            'start_date',
            'end_date',
            'location',
            'created_at',
            'updated_at'
        ]

class ArtworkSerializer(serializers.ModelSerializer):
    exhibition = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Artwork
        fields = [
            'id',
            'title',
            'description',
            'image',
            'metadata',
            'exhibition',
            'created_at',
            'updated_at'
        ]
