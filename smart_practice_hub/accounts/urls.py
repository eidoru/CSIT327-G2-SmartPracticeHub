from django.urls import include, path
from .views import CustomLoginView

from . import views

urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.CustomSignUpView.as_view(), name='signup'),
    path('home/', views.home, name='home'),
    path("practice/", views.practice_problems, name="practice_problems"),
    path("progress/", views.my_progress, name="my_progress"),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
]