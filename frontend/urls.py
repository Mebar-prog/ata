from django.contrib import admin
from django.urls import path
from frontend.views import *
# from django.contrib.auth import views as auth_views

app_name = 'frontend'

urlpatterns = [
    path('index/',index,name='index'),
    path('',admin_login,name='admin_login'),
    path('asset/<str:asset_id>/',asset_details, name='asset_details'),
    path('report_error/',report_error,name='report_error'), 
]