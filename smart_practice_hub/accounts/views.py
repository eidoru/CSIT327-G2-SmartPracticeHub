from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.db import models
from problems.models import Problem
from problems.models import Problem, ProblemProgress
from django.utils import timezone
from datetime import timedelta


from .forms import CustomUserCreationForm
from .forms import CustomAuthenticationForm
from .models import CustomUser
from django.contrib.auth.decorators import login_required

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

def home(request):
    # If user is authenticated, redirect based on role
    if request.user.is_authenticated:
        if request.user.role == 'teacher':
            return redirect('teacher_dashboard')
        elif request.user.role == 'student':
            return redirect('practice_problems')
    # If not authenticated, show the home page with login/signup options
    return render(request, 'home.html')  

@login_required
def practice_problems(request):
    # Get all problems from database
    problems = Problem.objects.all().order_by('-created_at')

    # Apply search filter
    search_query = request.GET.get('search', '').strip()
    if search_query:
        problems = problems.filter(
            Q(title__icontains=search_query) | 
            Q(problem_text__icontains=search_query) |
            Q(topic__icontains=search_query)
        )
    
    # Apply subject filter
    subject_filter = request.GET.get('subject', '').strip()
    if subject_filter:
        problems = problems.filter(subject=subject_filter)
    
    # Apply difficulty filter
    difficulty_filter = request.GET.get('difficulty', '').strip()
    if difficulty_filter:
        problems = problems.filter(difficulty=difficulty_filter)

    user_progress = {}
    if request.user.is_authenticated:
        # Both students and teachers can have progress
        progress_records = ProblemProgress.objects.filter(student=request.user)
        user_progress = {p.problem_id: p.status for p in progress_records}
    
    # Apply status filter
    status_filter = request.GET.get('status', '').strip()
    
    # Convert to format expected by template
    problems_list = []
    for problem in problems:
        progress_status = user_progress.get(problem.id, 'not_started')
        
        # Apply status filter
        if status_filter and progress_status != status_filter:
            continue
        
        problems_list.append({
            "id": problem.id,
            "title": problem.title,
            "description": problem.problem_text,
            "tags": [problem.subject, problem.topic],
            "difficulty": problem.difficulty,
            "type": "Practice Problem",
            "subject": problem.subject,
            "topic": problem.topic,
            "points": problem.points,
            "status": progress_status,
        })
    
    return render(request, "practice_problems.html", {"problems": problems_list})

@login_required
def my_progress(request):
    if request.user.role != 'student':
        # Redirect teachers to their dashboard
        return redirect('teacher_dashboard')
    
    # Get user's progress
    user_progress = ProblemProgress.objects.filter(student=request.user)
    
    # Calculate statistics
    total_problems = Problem.objects.count()
    completed_count = user_progress.filter(status='completed').count()
    in_progress_count = user_progress.filter(status='in_progress').count()
    correct_count = user_progress.filter(is_correct=True).count()
    total_attempts = user_progress.count()
    
    accuracy = (correct_count / total_attempts * 100) if total_attempts > 0 else 0
    
    # Get problems by subject
    math_problems = Problem.objects.filter(subject='Math').count()
    science_problems = Problem.objects.filter(subject='Science').count()
    
    # Get recent activity
    recent_progress = user_progress.order_by('-last_attempted')[:5]
    
    stats = [
        {"label": "Problems Solved", "value": completed_count, "subtext": f"out of {total_problems}"},
        {"label": "Accuracy Rate", "value": f"{accuracy:.1f}%", "subtext": f"{correct_count} correct"},
        {"label": "In Progress", "value": in_progress_count, "subtext": "problems"},
        {"label": "Total Attempts", "value": total_attempts, "subtext": "practice sessions"},
    ]

    quick_practice = [
        {
            "name": "Mathematics", 
            "problem_count": math_problems, 
            "last_practiced": "Never" if not user_progress.filter(problem__subject='Math').exists() else "Recently"
        },
        {
            "name": "Science", 
            "problem_count": science_problems, 
            "last_practiced": "Never" if not user_progress.filter(problem__subject='Science').exists() else "Recently"
        },
    ]

    recent_activity = []
    for progress in recent_progress:
        if progress.status == 'completed':
            recent_activity.append({
                "icon": "✅", 
                "title": f"Completed: {progress.problem.title}", 
                "details": f"Score: {'Correct' if progress.is_correct else 'Incorrect'} • {progress.completed_at|timesince} ago"
            })
        elif progress.status == 'in_progress':
            recent_activity.append({
                "icon": "📘", 
                "title": f"Started: {progress.problem.title}", 
                "details": f"Progress: {progress.attempts} attempts • {progress.last_attempted|timesince} ago"
            })
    
    # Add placeholder if no activity
    if not recent_activity:
        recent_activity.append({
            "icon": "🎯", 
            "title": "No activity yet", 
            "details": "Start practicing to see your progress here!"
        })

    return render(request, "my_progress.html", {
        "stats": stats,
        "quick_practice": quick_practice,
        "recent_activity": recent_activity,
        "user_progress": user_progress,  # Pass progress for template
    })

@login_required
def teacher_dashboard(request):
    # Check if user is a teacher
    if request.user.role != 'teacher':
        raise PermissionDenied("Only teachers can access the teacher dashboard.")
    
    from django.db.models import Count, Avg
    
    # Get statistics for the dashboard
    total_problems = Problem.objects.count()
    math_problems = Problem.objects.filter(subject='Math').count()
    science_problems = Problem.objects.filter(subject='Science').count()
    
    # Get difficulty breakdown
    easy_problems = Problem.objects.filter(difficulty='Easy').count()
    medium_problems = Problem.objects.filter(difficulty='Medium').count()
    hard_problems = Problem.objects.filter(difficulty='Hard').count()
    
    # Get recent problems
    recent_problems = Problem.objects.order_by('-created_at')[:5]
    
    # Get problem performance statistics
    problem_stats = []
    for problem in Problem.objects.all():
        total_attempts = ProblemProgress.objects.filter(problem=problem).count()
        correct_attempts = ProblemProgress.objects.filter(problem=problem, is_correct=True).count()
        success_rate = (correct_attempts / total_attempts * 100) if total_attempts > 0 else 0
        
        problem_stats.append({
            'problem': problem,
            'total_attempts': total_attempts,
            'correct_attempts': correct_attempts,
            'success_rate': f'{success_rate:.1f}%',
            'avg_attempts': ProblemProgress.objects.filter(problem=problem).aggregate(Avg('attempts'))['attempts__avg'] or 0,
        })
    
    # Get engagement statistics
    total_students = ProblemProgress.objects.values('student').distinct().count()
    total_attempts = ProblemProgress.objects.count()
    avg_success_rate = (ProblemProgress.objects.filter(is_correct=True).count() / total_attempts * 100) if total_attempts > 0 else 0
    
    # Get most attempted problems
    most_attempted = Problem.objects.annotate(
        attempt_count=Count('progress')
    ).order_by('-attempt_count')[:3]
    
    # Get most successful problems
    most_successful = Problem.objects.annotate(
        success_count=Count('progress', filter=models.Q(progress__is_correct=True))
    ).order_by('-success_count')[:3]
    
    context = {
        'total_problems': total_problems,
        'math_problems': math_problems,
        'science_problems': science_problems,
        'easy_problems': easy_problems,
        'medium_problems': medium_problems,
        'hard_problems': hard_problems,
        'recent_problems': recent_problems,
        'problem_stats': problem_stats,
        'total_students': total_students,
        'total_attempts': total_attempts,
        'avg_success_rate': f'{avg_success_rate:.1f}%',
        'most_attempted': most_attempted,
        'most_successful': most_successful,
    }
    
    return render(request, "teacher_dashboard.html", context)


@login_required
def teacher_students(request):
    # Only teachers should access this
    if request.user.role != 'teacher':
        raise PermissionDenied("Only teachers can view registered students.")

    # List all students
    students = CustomUser.objects.filter(role='student').order_by('first_name', 'last_name')

    return render(request, 'teacher_students.html', {
        'students': students,
    })

