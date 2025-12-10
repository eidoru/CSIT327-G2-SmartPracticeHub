from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import UserManager


class User(AbstractUser):
    STUDENT = 'student'
    TEACHER = 'teacher'

    ROLE_CHOICES = {
        STUDENT: 'Student',
        TEACHER: 'Teacher',
    }

    username = None

    email = models.EmailField(unique=True)
    role = models.CharField(choices=ROLE_CHOICES, default=STUDENT)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'role']

    def __str__(self):
        return self.email
