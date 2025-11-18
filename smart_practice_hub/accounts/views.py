# from django.contrib.auth.views import LoginView
# from django.contrib.auth.views import LogoutView
# from django.shortcuts import render, redirect
# from django.urls import reverse_lazy
# from django.views.generic import CreateView
# from django.contrib.auth.decorators import login_required
# from django.core.exceptions import PermissionDenied
# from problems.models import Problem
# from problems.models import Problem, ProblemProgress
# from django.utils import timezone
# from datetime import timedelta


# from .forms import CustomUserCreationForm
# from .forms import CustomAuthenticationForm

# class CustomSignUpView(CreateView):
#     form_class = CustomUserCreationForm
#     template_name = 'accounts/signup.html'
#     success_url = reverse_lazy('login')

# class CustomLoginView(LoginView):
#     template_name = 'accounts/login.html'
#     authentication_form = CustomAuthenticationForm
#     redirect_authenticated_user = True

# class CustomLogoutView(LogoutView):
#     next_page = reverse_lazy("home")
#     from django.shortcuts import render

# def home(request):
#     # If user is authenticated, redirect based on role
#     if request.user.is_authenticated:
#         if request.user.role == 'teacher':
#             return redirect('teacher_dashboard')
#         elif request.user.role == 'student':
#             return redirect('practice_problems')
#     # If not authenticated, show the home page with login/signup options
#     return render(request, 'home.html')  

# @login_required
# def practice_problems(request):
#     # Get all problems from database
#     problems = Problem.objects.all().order_by('-created_at')

#     user_progress = {}
#     if request.user.is_authenticated:
#         # Both students and teachers can have progress
#         progress_records = ProblemProgress.objects.filter(student=request.user)
#         user_progress = {p.problem_id: p.status for p in progress_records}
    
#     # Convert to format expected by template
#     problems_list = []
#     for problem in problems:
#         problems_list.append({
#             "id": problem.id,
#             "title": problem.title,
#             "description": problem.problem_text,
#             "tags": [problem.subject, problem.topic],
#             "difficulty": problem.difficulty,
#             "type": "Practice Problem",
#             "subject": problem.subject,
#             "topic": problem.topic,
#             "points": problem.points,
#             "status": user_progress.get(problem.id, 'not_started'),
#         })
#     return render(request, "practice_problems.html", {"problems": problems_list})

# @login_required
# def my_progress(request):
#     if request.user.role != 'student':
#         # Redirect teachers to their dashboard
#         return redirect('teacher_dashboard')
    
#     # Get user's progress
#     user_progress = ProblemProgress.objects.filter(student=request.user)
    
#     # Calculate statistics
#     total_problems = Problem.objects.count()
#     completed_count = user_progress.filter(status='completed').count()
#     in_progress_count = user_progress.filter(status='in_progress').count()
#     correct_count = user_progress.filter(is_correct=True).count()
#     total_attempts = user_progress.count()
    
#     accuracy = (correct_count / total_attempts * 100) if total_attempts > 0 else 0
    
#     # Get problems by subject
#     math_problems = Problem.objects.filter(subject='Math').count()
#     science_problems = Problem.objects.filter(subject='Science').count()
    
#     # Get recent activity
#     recent_progress = user_progress.order_by('-last_attempted')[:5]
    
#     stats = [
#         {"label": "Problems Solved", "value": completed_count, "subtext": f"out of {total_problems}"},
#         {"label": "Accuracy Rate", "value": f"{accuracy:.1f}%", "subtext": f"{correct_count} correct"},
#         {"label": "In Progress", "value": in_progress_count, "subtext": "problems"},
#         {"label": "Total Attempts", "value": total_attempts, "subtext": "practice sessions"},
#     ]

#     quick_practice = [
#         {
#             "name": "Mathematics", 
#             "problem_count": math_problems, 
#             "last_practiced": "Never" if not user_progress.filter(problem__subject='Math').exists() else "Recently"
#         },
#         {
#             "name": "Science", 
#             "problem_count": science_problems, 
#             "last_practiced": "Never" if not user_progress.filter(problem__subject='Science').exists() else "Recently"
#         },
#     ]

#     recent_activity = []
#     for progress in recent_progress:
#         if progress.status == 'completed':
#             recent_activity.append({
#                 "icon": "✅", 
#                 "title": f"Completed: {progress.problem.title}", 
#                 "details": f"Score: {'Correct' if progress.is_correct else 'Incorrect'} • {progress.completed_at|timesince} ago"
#             })
#         elif progress.status == 'in_progress':
#             recent_activity.append({
#                 "icon": "📘", 
#                 "title": f"Started: {progress.problem.title}", 
#                 "details": f"Progress: {progress.attempts} attempts • {progress.last_attempted|timesince} ago"
#             })
    
#     # Add placeholder if no activity
#     if not recent_activity:
#         recent_activity.append({
#             "icon": "🎯", 
#             "title": "No activity yet", 
#             "details": "Start practicing to see your progress here!"
#         })

#     return render(request, "my_progress.html", {
#         "stats": stats,
#         "quick_practice": quick_practice,
#         "recent_activity": recent_activity,
#         "user_progress": user_progress,  # Pass progress for template
#     })

# @login_required
# def teacher_dashboard(request):
#     # Check if user is a teacher
#     if request.user.role != 'teacher':
#         raise PermissionDenied("Only teachers can access the teacher dashboard.")
    
#     # Get statistics for the dashboard
#     total_problems = Problem.objects.count()
#     math_problems = Problem.objects.filter(subject='Math').count()
#     science_problems = Problem.objects.filter(subject='Science').count()
    
#     # Get recent problems
#     recent_problems = Problem.objects.order_by('-created_at')[:5]
    
#     context = {
#         'total_problems': total_problems,
#         'math_problems': math_problems,
#         'science_problems': science_problems,
#         'recent_problems': recent_problems,
#     }
    
#     return render(request, "teacher_dashboard.html", context)

from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView

from .forms import AccountCreationForm
from .forms import AccountLoginForm


def signup_view(request):
    if request.method == 'POST':
        form = AccountCreationForm(request.POST)

        print(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = AccountCreationForm()

    return render(request, 'accounts/signup.html', {'form': form})


class AccountLoginView(LoginView):
    template_name = 'accounts/login.html'
    next_page = 'dashboard'
    authentication_form = AccountLoginForm


class AccountLogoutView(LogoutView):
    next_page = 'login'