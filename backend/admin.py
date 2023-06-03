from django.contrib import admin
from backend.models import Asset, AssetCategory,InactiveAsset,ReportLog

class AssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'name', 'category', 'location', 'owner', 'purchase_date','qr_code','is_active')
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


class InactiveAssetAdmin(admin.ModelAdmin):
    list_display = ('asset_id', 'name', 'category', 'location', 'owner', 'purchase_date', 'qr_code','is_active')
    search_fields = ('asset__asset_id', 'asset__name')

    def asset_id(self, obj):
        return obj.asset.asset_id

    def name(self, obj):
        return obj.asset.name

    def category(self, obj):
        return obj.asset.category

    def location(self, obj):
        return obj.asset.location

    def owner(self, obj):
        return obj.asset.owner

    def purchase_date(self, obj):
        return obj.asset.purchase_date

    def qr_code(self, obj):
        return obj.asset.qr_code
    
    def is_active(self, obj):
        return obj.asset.is_active

admin.site.register(InactiveAsset, InactiveAssetAdmin)


from django.contrib import admin
from backend.models import ReportLog

class ReportLogAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'description', 'asset', 'service_type', 'remark', 'item_creation_date', 'completion_date', 'completed_by')
    list_filter = ('completion_date',)
    search_fields = ('name', 'asset__asset_id', 'completed_by__username')

admin.site.register(ReportLog, ReportLogAdmin)


