from django.shortcuts import redirect
from functools import wraps


def guest_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if user.is_authenticated:
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view