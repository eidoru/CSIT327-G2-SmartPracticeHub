from django.urls import path

from .views import landing_view
from .views import dashboard_view

from .views import student_dashboard_view
from .views import practice_problems_view

from .views import teacher_dashboard_view
from .views import problems_view

urlpatterns = [
    path('', landing_view, name='landing'),
    path('dashboard/', dashboard_view, name='dashboard'),

    path('student/dashboard/', student_dashboard_view, name='student_dashboard'),
    path('student/practice/', practice_problems_view, name='practice_problems'),

    path('teacher/dashboard/', teacher_dashboard_view, name='teacher_dashboard'),
    path('teacher/problems/', problems_view, name='problems'),
]
