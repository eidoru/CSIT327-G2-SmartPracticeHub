from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.EmailField()


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'role']
