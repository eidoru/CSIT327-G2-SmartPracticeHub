# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin

# from .forms import CustomUserCreationForm
# from .forms import CustomUserChangeForm

# from .models import CustomUser

# @admin.register(CustomUser)
# class CustomUserAdmin(UserAdmin):
#     add_form = CustomUserCreationForm
#     form = CustomUserChangeForm
#     model = CustomUser

#     list_display = ("email", "first_name", "last_name", "role", "is_staff", "is_active")
#     list_filter = ("role", "is_staff", "is_active")
#     ordering = ("email",)
#     search_fields = ("email", "first_name", "last_name")

#     fieldsets = (
#         (None, {"fields": ("email", "password")}),
#         ("Personal info", {"fields": ("first_name", "last_name", "role")}),
#         ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
#         ("Important dates", {"fields": ("last_login", "date_joined")}),
#     )

#     add_fieldsets = (
#         (None, {
#             "classes": ("wide",),
#             "fields": ("email", "first_name", "last_name", "role", "password1", "password2", "is_staff", "is_superuser", "is_active"),
#         }),
#     )

from django.contrib import admin

from .models import User


admin.site.register(User)