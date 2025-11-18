from django.urls import path

from .views import practice_view


urlpatterns = [
    path('<str:id>/', practice_view, name='practice'),
]
