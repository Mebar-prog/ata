from django.shortcuts import render
from django.contrib.auth import authenticate, login
# from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
import random

# Create your views here.
def index(request):
    return render(request, 'index-3.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')


def report_error(request):
    return render(request, 'report_error.html')


def admin_login(request):
    if request.method == 'POST':
        # Get the username and password from the request object
        username = request.POST['username']
        password = request.POST['password']
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # If the user is authenticated, log them in and redirect to the dashboard
        if user is not None:
            login(request, user)
            return redirect('backend:dashboard')    
        # If the user is not authenticated, show an error message
        else:
            messages.error(request, 'Invalid username or password')
    
    # If the request method is not POST, render the login page
    return render(request, 'login.html')

# asset details view with data retrived from backend app models
from django.shortcuts import render, get_object_or_404
from backend.models import Asset

def asset_details(request, asset_id):
    asset = get_object_or_404(Asset, asset_id=asset_id)
    return render(request, 'detail.html', {'asset': asset})

# reset password
def forgot_password(request):
    return render(request, 'password_reset.html')

from django.contrib.auth.models import User, Group

