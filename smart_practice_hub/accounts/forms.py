# from django import forms
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
# from .models import CustomUser

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'first_name', 'last_name', 'role')

# class CustomUserChangeForm(UserChangeForm):
#     class Meta:
#         model = CustomUser
#         fields = ('email', 'first_name', 'last_name', 'role', 'is_active', 'is_active')

# class CustomAuthenticationForm(AuthenticationForm):
#     username = forms.EmailField(
#         label="Email",
#         widget=forms.EmailInput(attrs={"autofocus": True})
#     )

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm

from .models import User


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2', 'role']


class AccountLoginForm(AuthenticationForm):
    username = forms.EmailField(label='Email')