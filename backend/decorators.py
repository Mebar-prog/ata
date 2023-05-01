from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import Group

def state_user_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.groups.filter(name='state_user').exists():
            return view_func(request, *args, **kwargs)
        else:
            raise PermissionDenied
    return wrapper
