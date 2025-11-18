# from django.contrib.auth import models

# class CustomUserManager(models.BaseUserManager):
#     use_in_migrations = True

#     def create_user(self, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError("The email must be set")
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)

#         if password:
#             user.set_password(password)
#         else:
#             raise ValueError("The password must be set")
        
#         user.save(using=self.db)
#         return user

#     def create_superuser(self, email, password=None, **extra_fields):
#         if password is None:
#             raise ValueError("Superusers must have a password.")
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_active", True)

#         if extra_fields.get("is_staff") is not True:
#             raise ValueError("Superuser must have is_staff=True.")
#         if extra_fields.get("is_superuser") is not True:
#             raise ValueError("Superuser must have is_superuser=True.")

#         return self.create_user(email, password, **extra_fields)

from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('User must have an email address')
        
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(email, password, **extra_fields)