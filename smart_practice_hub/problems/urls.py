from django.urls import path

from . import views


urlpatterns = [
    path('teacher/problems/add/', views.add_problem, name='add_problem'),
    path('teacher/problems/edit/<int:id>/', views.update_problem, name='edit_problem'),
    path('teacher/problems/delete/<int:id>/', views.delete_problem, name='delete_problem'),

    # API routes
    path('api/create/', views.create_problem_api, name='create_problem_api'),
    path('api/problems/<int:id>/update/', views.update_problem_api, name='update_problem_api'),
    path('api/problems/<int:id>/delete/', views.delete_problem_api, name='delete_problem_api'),

    path('<int:id>/answer/', views.answer_problem, name='answer_problem'),
    path('my-progress/', views.my_progress, name='my_progress'),
    path('problems/<int:id>/answer/', views.answer_problem, name='answer_problem'),
]
