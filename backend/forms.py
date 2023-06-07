from django import forms

class AssetUploadForm(forms.Form):
    file = forms.FileField(label='Excel File')
