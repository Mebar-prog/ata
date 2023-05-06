from rest_framework import serializers
from backend.models import Asset

class DormAmenitiesAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ('asset_id', 'name', 'category', 'sub_category', 'location', 'owner',)
        read_only_fields = ('asset_id', 'name', 'category', 'sub_category', 'location',)
