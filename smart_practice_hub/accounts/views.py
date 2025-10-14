from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm

class CustomSignUpView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'
    authentication_form = CustomAuthenticationForm
    redirect_authenticated_user = True

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("home")
    from django.shortcuts import render

def practice_problems(request):
    problems = [
        {
            "title": "Newton's Second Law",
            "description": "A 10kg object accelerates at 5m/s². What is the net force acting on the object?",
            "tags": ["Physics", "Mechanics"],
            "difficulty": "Hard",
            "type": "Short Answer"
        },
        {
            "title": "Chemical Bonding",
            "description": "Ionic bonds form between metals and non-metals through the transfer of electrons.",
            "tags": ["Chemistry", "Atomic Structure"],
            "difficulty": "Easy",
            "type": "True/False"
        },
        {
            "title": "Quadratic Equations",
            "description": "Solve the quadratic equation: x² - 5x + 6 = 0",
            "tags": ["Mathematics", "Algebra"],
            "difficulty": "Medium",
            "type": "Multiple Choice"
        },
    ]
    return render(request, "practice_problems.html", {"problems": problems})

def my_progress(request):
    stats = [
        {"label": "Problems Solved", "value": 0, "subtext": ""},
        {"label": "Accuracy Rate", "value": "?%", "subtext": ""},
        {"label": "Study Streak", "value": "?", "subtext": "days in a row"},
        {"label": "Time Practiced", "value": "? hours", "subtext": "this month"},
    ]

    quick_practice = [
        {"name": "Mathematics", "problem_count": 0, "last_practiced": "?"},
        {"name": "Physics", "problem_count": 0, "last_practiced": "? days ago"},
    ]

    recent_activity = [
        {"icon": "✅", "title": "Completed ? Set #?", "details": "Score: ? • ? hours ago"},
        {"icon": "📘", "title": "Started ?: ?", "details": "Progress: ? • ?"},
        {"icon": "🏆", "title": "Achievement Unlocked!", "details": "?-day streak • ? days ago"},
    ]

    return render(request, "my_progress.html", {
        "stats": stats,
        "quick_practice": quick_practice,
        "recent_activity": recent_activity,
    })
