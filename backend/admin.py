from django.contrib import admin
from backend.models import Asset, AssetCategory

class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'name', 'category', 'location', 'owner', 'purchase_date','qr_code')
    list_filter = ('category','location', 'owner')
    search_fields = ('asset_id', 'name', 'category__name','location', 'owner')

admin.site.register(Asset, AssetAdmin)
admin.site.register(AssetCategory)

from backend.models import Asset, Report

class AssetReportAdmin(admin.ModelAdmin):
    list_display = ('asset', 'name', 'email', 'service_type', 'description', 'remark')
    list_filter = ('asset',)
    search_fields = ('asset__asset_id', 'name', 'email', 'description')

admin.site.register(Report, AssetReportAdmin)

