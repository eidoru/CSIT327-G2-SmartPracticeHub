# from django.urls import include, path
# from .views import CustomLoginView

# from . import views

# urlpatterns = [
#     path('login/', views.CustomLoginView.as_view(), name='login'),
#     path('logout/', views.CustomLogoutView.as_view(), name='logout'),
#     path('signup/', views.CustomSignUpView.as_view(), name='signup'),
#     path('home/', views.home, name='home'),
#     path("practice/", views.practice_problems, name="practice_problems"),
#     path("progress/", views.my_progress, name="my_progress"),
#     path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
# ]

from django.urls import path

from .views import signup_view
from .views import AccountLoginView
from .views import AccountLogoutView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
]
