from django.shortcuts import redirect
from django.urls import reverse

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
class StateUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and (request.user.groups.filter(name='state_user').exists() or request.user.groups.filter(name='ict_user').exists()):
            request.is_state_user = True  # Add the flag here
            if not request.path.startswith(reverse('backend:report')) and not request.path.startswith(
                    reverse('backend:report_remark')) and not request.path.startswith(
                    reverse('backend:update_admin_profile')) and not request.path.startswith(reverse('backend:profile')):
                if not request.path.startswith(reverse('backend:logout')):
                    return redirect('backend:report')
        response = self.get_response(request)
        return response
