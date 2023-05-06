from django.urls import path
from api.views import *
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [
    path('account/v1/generatetoken/', obtain_auth_token, name='api_token_auth'),
    path('assets/v1/dorm_amenities', DormAmenitiesAssetList.as_view(), name='dorm_amenities_asset_list'),
    path('assets/v1/dorm_amenities/<int:pk>/', DormAmenitiesAssetUpdate.as_view(), name='dorm_amenities_asset_update'),
]

