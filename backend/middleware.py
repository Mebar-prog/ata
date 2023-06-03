# class StateUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated and request.user.groups.filter(name='state_user').exists():
#             request.is_state_user = True # Add the flag here
#             if not request.path.startswith(reverse('backend:report')) and not request.path.startswith(reverse('backend:report_remark')) and not request.path.startswith(reverse('backend:update_admin_profile')) and not request.path.startswith(reverse('backend:profile')):
#                 if not request.path.startswith(reverse('backend:logout')):
#                     return redirect('backend:report')
#         response = self.get_response(request)
#         return response

# ict user 
# class StateUserMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if request.user.is_authenticated and (request.user.groups.filter(name='state_user').exists() or request.user.groups.filter(name='ict_user').exists()):
#             request.is_state_user = True  # Add the flag here
#             if not request.path.startswith(reverse('backend:report')) and not request.path.startswith(
#                     reverse('backend:report_remark')) and not request.path.startswith(
#                     reverse('backend:export_report_as_excel')) and not request.path.startswith(
#                     reverse('backend:update_admin_profile')) and not request.path.startswith(reverse('backend:profile')):
#                 if not request.path.startswith(reverse('backend:logout')):
#                     return redirect('backend:report')
#         response = self.get_response(request)
#         return response

from backend.views import move_report_to_log,delete_report,delete_log
from django.urls import reverse
from django.shortcuts import redirect

class StateUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and (request.user.groups.filter(name='state_user').exists() or request.user.groups.filter(name='ict_user').exists()):
            request.is_state_user = True 

            allowed_paths = [
                reverse('backend:report'),
                reverse('backend:report_remark'),
                reverse('backend:export_report_as_excel'),
                reverse('backend:update_admin_profile'),
                reverse('backend:profile'),
                reverse('backend:report_log'),
                reverse('backend:export_report_log_as_excel'),
                
            ]
            
            if request.path not in allowed_paths:
                if not request.path.startswith(reverse('backend:logout')):
                    if 'move_report_to_log' in request.path:
                        # Handle move_report_to_log separately
                        report_id = request.path.split('/')[-3]  # Extract the report_id from the URL
                        return move_report_to_log(request, report_id)  # Call the view function directly
                    
                    elif 'delete_report' in request.path:
                        # Handle delete_report separately
                        report_id = request.path.split('/')[-3]  
                        return delete_report(request, report_id)
                    
                    elif 'delete_log' in request.path:
                        report_log_id = request.path.split('/')[-2]
                        return delete_log(request, report_log_id)
                     
                    else:
                        return redirect('backend:report')

        response = self.get_response(request)
        return response








