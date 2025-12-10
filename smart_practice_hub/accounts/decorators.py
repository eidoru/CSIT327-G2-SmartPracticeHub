from django.shortcuts import redirect
from functools import wraps


def student_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('landing')

        if getattr(user, 'role', None) != 'student':
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def teacher_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        user = request.user

        if not user.is_authenticated:
            return redirect('landing')

        if getattr(user, 'role', None) != 'teacher':
            return redirect('dashboard')
        return view_func(request, *args, **kwargs)
    return _wrapped_view