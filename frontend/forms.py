from django import forms
from django.contrib.auth.forms import PasswordResetForm

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField()

    def send_password_reset_email(self, request):
        email = self.cleaned_data['email']
        PasswordResetForm({'email': email}).save(request=request, use_https=True)
