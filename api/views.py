from rest_framework import generics, permissions
from rest_framework.authentication import TokenAuthentication
from backend.models import Asset
from api.serializers import DormAmenitiesAssetSerializer

class DormAmenitiesAssetList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DormAmenitiesAssetSerializer

    def get_queryset(self):
        return Asset.objects.filter(category__category_name='dorm_amenities')


class DormAmenitiesAssetUpdate(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Asset.objects.filter(category__category_name='dorm_amenities')
    serializer_class = DormAmenitiesAssetSerializer

