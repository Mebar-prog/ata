from import_export import resources
from backend.models import Asset,AssetCategory

class AssetResource(resources.ModelResource):
    class meta:
        model = Asset 
        fields = ('asset_id', 'name', 'category', 'sub_category', 'location', 'owner', 'purchase_date')



