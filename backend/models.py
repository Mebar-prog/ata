from django.db import models
import qrcode
from io import BytesIO
from django.core.files.base import ContentFile
from django.utils import timezone
from django.contrib.auth.models import User, Group
import urllib.parse


# Create your models here. 
class AssetCategory(models.Model):
    category_name = models.CharField(max_length=100,null=True)
    item_creation_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.category_name or ''
    

class Asset(models.Model):
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)
    asset_id = models.CharField(max_length=100, unique=True, primary_key=True)
    name = models.CharField(max_length=100)
    category = models.ForeignKey('AssetCategory', on_delete=models.CASCADE)
    location = models.CharField(max_length=100,null=True)
    owner = models.CharField(max_length=100)
    purchase_date = models.DateField()
    item_creation_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.asset_id

    def generate_qr_code(self):
        # Get the base URL of your website
        base_url = 'https://ata-n6du.onrender.com/'
        # base_url = 'http://127.0.0.1:8000/'

        # Create the full URL for this asset's detail page
        # asset_url = f'{base_url}asset/{self.asset_id}/'
        encoded_asset_id = urllib.parse.quote(self.asset_id, safe='')
        asset_url = f'{base_url}asset/{encoded_asset_id}/'
        # Encode the URL for use in a QR code
        # encoded_url = urllib.parse.quote(asset_url, safe='')
  
        # Create the QR code object
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        # Add the encoded URL to the QR code
        qr.add_data(asset_url)
        qr.make(fit=True)
        # Generate the QR code image
        img = qr.make_image(fill_color='black', back_color='white')
        # Create an in-memory buffer to store the image data
        buffer = BytesIO()
        # Save the image to the buffer in PNG format
        img.save(buffer, format='PNG')
        # Create a Django ContentFile from the buffer data
        file = ContentFile(buffer.getvalue())
        # Create an InMemoryUploadedFile from the ContentFile
        file_name = f"{self.asset_id}.png"
        self.qr_code.save(file_name, file)

    def save(self, *args, **kwargs):
        # Check if qr_code field has been set yet
        if not self.qr_code:
            # Generate the QR code for this asset
            self.generate_qr_code()
        # Call the parent class's save method
        super().save(*args, **kwargs)


class InactiveAsset(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return self.asset.asset_id

class Report(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    description = models.TextField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100, default='none') 
    remark = models.TextField(blank=True, null=True)
    item_creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.asset.asset_id}'

class ReportLog(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    description = models.TextField()
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=100, default='none') 
    remark = models.TextField(blank=True, null=True)
    item_creation_date = models.DateTimeField()

    completion_date = models.DateTimeField(auto_now_add=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f'Report Log - {self.name} - {self.asset.asset_id}'









