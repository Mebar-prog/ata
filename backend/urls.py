from django.contrib import admin
from django.urls import path
from backend.views import *

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path


app_name = 'backend'

urlpatterns = [
    path('', staff_member_required(dashboard), name='dashboard'),
    path('profile/',login_required(profile),name='profile'),
    path('manageasset/',manageasset,name='manageasset'),
    path('upload_assets/',upload_assets,name='upload_assets'),#bulk asset 
    path('export_to_excel/',export_to_excel,name='export_to_excel'),
    path('logout/', logout_view, name='logout'),
    path('profile', update_admin_profile, name='update_admin_profile'),
    path('users/', user_list, name='user_list'),
    path('user/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('add_user/', add_user, name='add_user'),
    path('category/',category,name='category'),
    path('category/<int:category_id>/', category_table, name='category_table'),
    path('report/',report,name='report'),
    path('report_remark/',report_remark, name='report_remark'),

    path('delete_report/<int:report_id>/delete/', delete_report, name='delete_report'),
    # re_path(r'^report/(?P<report_id>[0-9a-zA-Z]+)/delete/$', delete_report, name='delete_report'),
    # re_path(r'^report/(?P<report_id>[0-9]+)/delete/$', delete_report, name='delete_report'),

    
    path('save_report/', save_report, name='save_report'),
    # path('asset/<str:asset_id>/',asset_details, name='asset_details'),
    path('add-asset/',add_asset,name='add_asset'),
    path('edit_asset/',edit_asset, name='edit_asset'),
    # path('transfer_asset/<str:asset_id>/', transfer_asset, name='transfer_asset'),
    re_path(r'^transfer_asset/(?P<asset_id>.+)/$', transfer_asset, name='transfer_asset'),


    # path('delete_asset/<str:asset_id>/',delete_asset, name='delete_asset'),
    re_path(r'^delete_asset/(?P<asset_id>.+)/$',delete_asset, name='delete_asset'),


    path('add_category/', add_category, name='add_category'),
    path('delete_category/<int:id>/',delete_category, name='delete_category'),
    path('edit_category/',edit_category, name='edit_category'),
    # path('print_qr_codes/', print_qr_codes, name='print_qr_codes'),
    path('print_qr_codes/', print_qr_codes, name='print_qr_codes'),
    path('print_qr_codes_with_loading/', print_qr_codes_with_loading, name='print_qr_codes_with_loading'),
    path('export/', export_report_as_excel, name='export_report_as_excel'),
    path('inactive-assets/', inactive_assets, name='inactive_assets'),
    # path('activate_asset/<str:asset_id>/', activate_asset, name='activate_asset'),
    re_path(r'^activate_asset/(?P<asset_id>.+)/$',activate_asset, name='activate_asset'),

    path('export_inactive_to_excel/', export_inactive_to_excel, name='export_inactive_to_excel'),
    path('report_log/',report_log,name='report_log'),

    re_path(r'^move_report_to_log/(?P<report_id>[0-9]+)/remove/$', move_report_to_log, name='move_report_to_log'),


    path('delete_log/<int:report_log_id>/', delete_log, name='delete_log'),

    path('export-report-log-as-excel/', export_report_log_as_excel, name='export_report_log_as_excel'),

    
]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)