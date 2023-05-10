from django.contrib.auth import logout
from django.urls import reverse
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from backend.models import Asset,AssetCategory,Report
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib import messages
from datetime import datetime
from openpyxl import load_workbook
from openpyxl import Workbook
from django.http import HttpResponse
from django.conf import settings
import os

# import qrcode
# from io import BytesIO
# from django.core.files import File
from django.http import FileResponse
from openpyxl import Workbook

# Create your views here.
@login_required
def dashboard(request):
    assets = Asset.objects.order_by('-item_creation_date')[:5]
    a = Asset.objects.all()
    category = AssetCategory.objects.all()
    total_category = category.count()
    total_assets = a.count()
    total_owners = Asset.objects.values('owner').distinct().count()
    context = {
        'assets': assets,
        'total_assets': total_assets,
        'total_category': total_category,
        'category': category,
        'a': a,
        'total_owners': total_owners,
     }
    return render(request, 'index.html',context)


@login_required
def manageasset(request):
    assets = Asset.objects.order_by('-item_creation_date')
    paginator = Paginator(assets, 10 ) # Show 5 assets per page

    page = request.GET.get('page')
    try:
        assets = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        assets = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        assets = paginator.page(paginator.num_pages)

    context = {
        'assets': assets,
        'category': AssetCategory.objects.all()
    }

    return render(request, 'tables.html', context)

# search in tables.html
@login_required
def asset_list(request):
  search_term = request.GET.get('search_term')
  if search_term:
    assets = Asset.objects.filter(asset_id=search_term)
  else:
    assets = Asset.objects.all()
  context = {'assets': assets}
  return render(request, 'tables.html', context)



# category view with pagination
@login_required
def category(request):
    category = AssetCategory.objects.all()
    categories_list = AssetCategory.objects.order_by('-item_creation_date')
    paginator = Paginator(categories_list, 3) # Show 10 categories per page

    page = request.GET.get('page')
    try:
        categories = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        categories = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        categories = paginator.page(paginator.num_pages)

    context = {
        'categories': categories,
        'category':category,
    }
    return render(request, 'category.html', context)


# add category
@login_required
def add_category(request):
    if request.method == 'POST':
        category_name = request.POST.get('category_name')
        category = AssetCategory.objects.create(category_name=category_name)
        return redirect('backend:category')
    else:
        return render(request, 'category.html')

#delete category
@login_required
def delete_category(request,id):
    c = get_object_or_404(AssetCategory, id=id)
    c.delete()
    return redirect(reverse('backend:category'))

# edit category
@login_required
def edit_category(request):
    if request.method == 'POST':
        c_id = request.POST['id']
        cat = get_object_or_404(AssetCategory, id=c_id)
        cat.category_name = request.POST['category_name']
        cat.save()
        return redirect('backend:category')

    return render(request, 'category.html')

# same category asset table view
@login_required
def category_table(request, category_id):
    category = AssetCategory.objects.get(id=category_id)
    asset_list = Asset.objects.filter(category=category)

    # search functionality
    search_term = request.GET.get('search_term')
    if search_term:
        asset_list = asset_list.filter(asset_id__icontains=search_term.lower())

    paginator = Paginator(asset_list, 10) # Show 10 assets per page
    page = request.GET.get('page')
    assets = paginator.get_page(page)
    category_name = category.category_name
    category = AssetCategory.objects.all()
    return render(request, 'category_table.html', {'category': category, 'assets': assets,'category_name': category_name})


# report view
@login_required
def report(request):
    category = AssetCategory.objects.all()
    report_list = Report.objects.order_by('item_creation_date').all()
    # Handle search functionality
    search_term = request.GET.get('search_term')
    if search_term:
        report_list = report_list.filter(asset__asset_id__icontains=search_term)

    paginator = Paginator(report_list, 2) # Show 2 reports per page
    page = request.GET.get('page')
    reports = paginator.get_page(page)
    context = {
        'category': category,
        'reports': reports,
        'search_term': search_term,
    }
    return render(request, 'report.html', context)


# report remark view
@login_required
def report_remark(request):
    if request.method == 'POST':
        asset_id = request.POST['id']
        r = get_object_or_404(Report, asset_id=asset_id)
        r.remark = request.POST['remark']
        r.save()
        return redirect('backend:report')

# delete report 
@login_required
def delete_report(request, report_id):
    if request.method == 'POST':
        report = get_object_or_404(Report, asset__asset_id=report_id)
        report.delete()
        return redirect('backend:report')



# logout view
@login_required
def logout_view(request):
    logout(request)
    return redirect('frontend:admin_login')



# password change
@login_required
def profile(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid() and (request.user.is_staff or request.user.is_superuser):
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect(reverse('backend:profile'))
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    if request.user.is_staff or request.user.is_superuser:
        category = AssetCategory.objects.all()
        return render(request, 'profile.html', {'form': form,'category':category,})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('backend:profile'))




# username and email change
@login_required
def update_admin_profile(request):
    if request.method == 'POST':
        user = request.user
        if user.is_staff or user.is_superuser:
            user.username = request.POST.get('username')
            user.email = request.POST.get('email')
            user.save()
            return redirect(reverse('backend:profile'))
    return render(request, 'profile.html')



# list the users baased table based on role
@login_required
def user_list(request):
    if request.user.is_superuser:
        users = User.objects.select_related('groups').all()
        category = AssetCategory.objects.all()
        context = {'users': users,'category': category}
        return render(request, 'users.html', context)
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('backend:dashboard'))

# manage user table pagination
@login_required
def user_list(request):
    if request.user.is_superuser:
        user_list = User.objects.all()
        paginator = Paginator(user_list, 5) # Show 10 users per page

        page = request.GET.get('page')
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            users = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            users = paginator.page(paginator.num_pages)

        return render(request, 'users.html', {'users': users})
    else:
        messages.error(request, 'You do not have permission to access this page.')
        return redirect(reverse('backend:dashboard'))

# delete users
@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect(reverse('backend:user_list'))


#add user
@login_required
def add_user(request):
    if request.method == 'POST':
        # get form data
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        
        # validate form data
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return redirect('add_user')
        
        # create new user
        new_user = User.objects.create_user(username=username, email=email, password=password)
        
        # add role to new user
        if role == 'admin':
            new_user.is_superuser = True
            new_user.is_staff = True
            new_user.save()
        elif role == 'staff_user':
            new_user.is_staff = True
            new_user.save()
        elif role == 'state_user':
            group = Group.objects.get(name='state_user')
            new_user.groups.add(group)
            new_user.is_staff = True
            new_user.save()

            
        else:
            messages.error(request, 'Invalid role')
            return redirect(reverse('backend:user_list'))
        
        messages.success(request, 'User created successfully')
        return redirect(reverse('backend:user_list'))
    
    return render(request, 'users.html')


#Read qr code and display asset detail page
# from django.shortcuts import render, get_object_or_404
# from backend.models import Asset, AssetCategory

# def asset_details(request, asset_id):
#     asset = get_object_or_404(Asset, asset_id=asset_id)
#     return render(request, 'detail.html', {'asset': asset})


# adding asset details individually
@login_required
def add_asset(request):
    if request.method == 'POST':
        asset_id = request.POST['asset_id']
        name = request.POST['name']
        category_id = request.POST['category']
        category = AssetCategory.objects.get(id=category_id)
        sub_category = request.POST['sub_category']
        location = request.POST['location']
        owner = request.POST['owner']
        purchase_date = request.POST['purchase_date']
        asset = Asset(asset_id=asset_id, name=name, category=category, sub_category=sub_category, location=location, owner=owner, purchase_date=purchase_date)
        asset.save()
        
        return redirect(reverse('backend:manageasset')) 
    
    return render(request, 'tables.html')

# edit asset details
@login_required
def edit_asset(request):
    if request.method == 'POST':
        asset_id = request.POST['asset_id']
        asset = Asset.objects.get(asset_id=asset_id)
        asset.name = request.POST['name']
        category_id = request.POST['category']
        asset.category = AssetCategory.objects.get(id=category_id)
        asset.sub_category = request.POST['sub_category']
        asset.location = request.POST['location']
        asset.owner = request.POST['owner']
        asset.purchase_date = request.POST['purchase_date']
        asset.save()

        return redirect(reverse('backend:manageasset'))
    
    return render(request, 'tables.html')

# delete asset
@login_required 
def delete_asset(request,asset_id):
    asset_id = request.POST.get('asset_id')
    asset = Asset.objects.get(id=asset_id)
    asset.delete()
    return redirect(reverse('backend:manageasset'))

#delete asset 
def delete_asset(request, asset_id):
    asset = get_object_or_404(Asset, asset_id=asset_id)
    asset.delete()
    return redirect(reverse('backend:manageasset'))

# view of report of faulty asset
def save_report(request):
    if request.method == 'POST':
        # Get the form data
        asset_id = request.POST['asset_id']
        asset = Asset.objects.get(asset_id=asset_id)
        name = request.POST['name']
        email = request.POST['email']
        description = request.POST['description']

        # Check if a report object already exists for this asset
        if Report.objects.filter(asset=asset).exists():
            return redirect(reverse('frontend:report_error'))

        # Create a new report object
        report = Report.objects.create(
            name=name,
            email=email,
            description=description,
            asset=asset
        )
        
        user_emails = list(User.objects.values_list('email', flat=True))
        # Send email to all users in the system
        send_mail(
        'New Report Submitted',
        f'A new report has been submitted for asset id {asset_id}.\n\nName: {name}\nEmail: {email}\nDescription: {description}',
        'from@example.com',
        user_emails,
        fail_silently=False,
)

        return redirect('frontend:index')

    return render(request, 'frontend/detail.html')


# upload asset detail in bulk
@login_required
def upload_excel_file(request):
    if request.method == 'POST' and request.FILES['excel_file']:
        excel_file = request.FILES['excel_file']
        wb = load_workbook(excel_file)
        worksheet = wb['Sheet1']
        for row in worksheet.iter_rows(min_row=2, values_only=True):
            asset = Asset()
            asset.asset_id = row[0]
            asset.name = row[1]
            category_name = row[2]
            category, created = AssetCategory.objects.get_or_create(category_name=category_name)
            asset.category = category
            asset.sub_category = row[3]
            asset.location = row[4]
            asset.owner = row[5]
            purchase_date_str = row[6]
            asset.item_creation_date = datetime.now()
            if isinstance(purchase_date_str, datetime): # check if the variable is already in datetime format
                purchase_date = purchase_date_str.date()
            else:
                purchase_date = datetime.strptime(purchase_date_str, '%m/%d/%y').date() # format the date string to the expected format
            asset.purchase_date = purchase_date
            asset.save()

        messages.success(request, 'File Uploaded Successfully')
        return redirect(reverse('backend:manageasset'))

    return render(request, 'tables.html')


# export asset details in excel format
@login_required
def export_to_excel(request):
    # Create a new Excel workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active
    
    # Write the headers for the Excel file
    headers = ['Asset ID', 'Name', 'Category', 'Sub Category', 'Location', 'Owner', 'Purchase Date']
    ws.append(headers)
    
    # Write the asset data to the Excel file
    assets = Asset.objects.all().values_list(
        'asset_id', 'name', 'category__category_name', 'sub_category', 'location', 'owner', 'purchase_date'
    )
    for asset in assets:
        ws.append(asset)
    
    # Save the Excel file to a specific location
    file_path = os.path.join(settings.BASE_DIR, 'assets.xlsx')
    wb.save(file_path)
    
    # Check if the file exists
    if os.path.exists(file_path):
        # Open the saved file for reading
        with open(file_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename=assets.xlsx'
        return response
    else:
        return HttpResponse("File not found.")



# print qr code in bulk
@login_required
def print_qr(request):
    assets = Asset.objects.all()
    qr_codes = []
    for asset in assets:
        # Append the QR code and asset details to the list
        qr_codes.append({
            'qr_code': asset.qr_code,
            'asset_id': asset.asset_id,
            'name': asset.name,
            'category': asset.category.category_name,
            'sub_category': asset.sub_category,
            'location': asset.location,
            'owner': asset.owner,
        })
    
    # Render the template with the QR codes and asset details
    return render(request, 'print_qr.html', {'qr_codes': qr_codes})



























    




