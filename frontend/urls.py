from django.contrib import admin
from django.urls import path,re_path
from frontend.views import *
# from django.contrib.auth import views as auth_views

app_name = 'frontend'

urlpatterns = [
    path('',admin_login,name='admin_login'),
    path('index/',index,name='index'),
    path('report_error/',report_error,name='report_error'), 
    re_path(r'^asset/(?P<asset_id>.+)/$',asset_details, name='asset_details')
    # path('asset/<str:asset_id>/',asset_details, name='asset_details'),

]