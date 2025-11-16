from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_problem, name='add_problem'),
    path('api/create/', views.create_problem_api, name='create_problem_api'),
]
