from django.contrib import admin
from django.urls import path
from frontend.views import *
# from django.contrib.auth import views as auth_views

app_name = 'frontend'

urlpatterns = [
    path('index/',index,name='index'),
    path('about/',about,name='about'),
    path('contact/',contact,name='contact'),
    path('',admin_login,name='admin_login'),
    path('asset/<str:asset_id>/',asset_details, name='asset_details'),
    path('report_error/',report_error,name='report_error'),
    # path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    # path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_confirm/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),    
]