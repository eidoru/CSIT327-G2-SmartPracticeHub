from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views.decorators.http import require_POST

from .forms import SignupForm


@require_POST
def login_view(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        print("Success")
        return redirect('dashboard')
    
    print("Failure")
    return redirect('landing')


def logout_view(request):
    logout(request)
    return redirect('landing')


@require_POST
def signup_view(request):
    form = SignupForm(request.POST)

    if form.is_valid():
        form.save()
        return redirect('landing')
    
    print("Failure")
    print(form.errors)
    return redirect('landing')
