from rest_framework import generics, permissions,filters
from rest_framework.authentication import TokenAuthentication
from django_filters.rest_framework import DjangoFilterBackend

from backend.models import Asset
from api.serializers import DormAmenitiesAssetSerializer

# class DormAmenitiesAssetList(generics.ListAPIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = DormAmenitiesAssetSerializer

#     def get_queryset(self):
#         return Asset.objects.filter(category__category_name='dorm_amenities')
class DormAmenitiesAssetList(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DormAmenitiesAssetSerializer
    queryset = Asset.objects.filter(category__category_name='dorm_amenities')
    filter_backends = [filters.OrderingFilter, filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'location', 'owner']
    ordering_fields = ['name']
    filterset_fields = ['owner']  # Add this line to enable filtering by owner

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply additional filtering if needed
        return queryset


class DormAmenitiesAssetUpdate(generics.UpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    queryset = Asset.objects.filter(category__category_name='dorm_amenities')
    serializer_class = DormAmenitiesAssetSerializer

