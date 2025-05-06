from rest_framework import serializers
from kreative.marketplace.models import ArtistProfile, Commission, MarketplaceListing

class ArtistProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = ArtistProfile
        fields = [
            'id',
            'user',
            'biography',
            'portfolio_url',
            'metadata',
            'created_at',
            'updated_at'
        ]

class CommissionSerializer(serializers.ModelSerializer):
    requested_by = serializers.PrimaryKeyRelatedField(read_only=True)
    assigned_to = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Commission
        fields = [
            'id',
            'title',
            'description',
            'budget',
            'requested_by',
            'assigned_to',
            'status',
            'contract_url',
            'created_at',
            'updated_at'
        ]

class MarketplaceListingSerializer(serializers.ModelSerializer):
    artist_profile = ArtistProfileSerializer(read_only=True)

    class Meta:
        model = MarketplaceListing
        fields = [
            'id',
            'title',
            'description',
            'price',
            'image',
            'artist_profile',
            'status',
            'payment_details',
            'created_at',
            'updated_at'
        ]
