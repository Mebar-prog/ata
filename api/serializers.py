from rest_framework import serializers
from backend.models import Asset, AssetCategory

class AssetCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetCategory
        fields = ('id', 'category_name')

class DormAmenitiesAssetSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(source='category.category_name')

    class Meta:
        model = Asset
        fields = ('asset_id', 'name', 'category', 'location', 'owner',)
        read_only_fields = ('asset_id', 'name', 'category', 'location',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        return representation


