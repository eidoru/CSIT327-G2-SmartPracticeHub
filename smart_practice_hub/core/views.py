from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.db import models
from django.db.models import Count
from django.db.models import Avg
from django.db.models import Q
from django.shortcuts import render
from django.shortcuts import redirect

from .decorators import guest_required

from accounts.decorators import student_required
from accounts.decorators import teacher_required
from accounts.forms import LoginForm
from accounts.forms import SignupForm

from problems.models import Problem
from problems.models import ProblemProgress

from django.utils.timesince import timesince


@guest_required
def landing_view(request):
    login_form = LoginForm()
    signup_form = SignupForm()

    return render(request, 'core/landing.html', {
        'login_form': login_form,
        'signup_form': signup_form,
    })


@login_required
def dashboard_view(request):
    user = request.user

    if user.role == 'student':
        return redirect('student_dashboard')
    
    if user.role == 'teacher':
        return redirect('teacher_dashboard')
    

@student_required
def practice_problems_view(request):
    # Get all problems from database
    problems = Problem.objects.all().select_related('created_by').only(
        'id', 'title', 'problem_text', 'subject', 'topic', 'difficulty', 'points', 'created_by'
    ).order_by('-created_at')

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
        user_progress = {p.problem_id: {'status': p.status, 'is_correct': p.is_correct} for p in progress_records}
    
    # Apply status filter
    status_filter = request.GET.get('status', '').strip()
    
    # Convert to format expected by template
    problems_list = []
    for problem in problems:
        progress_data = user_progress.get(problem.id, {'status': 'not_started', 'is_correct': False})
        progress_status = progress_data['status']
        is_correct = progress_data['is_correct']
        
        # Apply status filter
        if status_filter and progress_status != status_filter:
            continue
        
        # Calculate score
        score = problem.points if (progress_status == 'completed' and is_correct) else 0
        
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
            "score": score,
            "is_correct": is_correct,
            "created_by": problem.created_by.get_full_name() if problem.created_by else "Unknown",
        })
    
    # Paginate results (10 per page)
    paginator = Paginator(problems_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Preserve query parameters except page
    query_params = request.GET.copy()
    query_params.pop('page', None)
    base_querystring = query_params.urlencode()

    return render(request, "core/practice_problems.html", {
        "problems": page_obj,
        "page_obj": page_obj,
        "base_querystring": base_querystring,
    })
    

@student_required
def student_dashboard_view(request):
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

    # Quick Practice
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

    # Recent Activity (PracticeSession)
    from problems.models import PracticeSession
    recent_sessions = PracticeSession.objects.filter(user=request.user).order_by('-started_at')[:5]

    # History Table (paginated PracticeSession)
    history_sessions = PracticeSession.objects.filter(user=request.user).order_by('-started_at')
    history_paginator = Paginator(history_sessions, 10)
    history_page_number = request.GET.get('history_page')
    history_page_obj = history_paginator.get_page(history_page_number)

    stats = [
        {"label": "Problems Solved", "value": completed_count, "subtext": f"out of {total_problems}"},
        {"label": "Accuracy Rate", "value": f"{accuracy:.1f}%", "subtext": f"{correct_count} correct"},
        {"label": "In Progress", "value": in_progress_count, "subtext": "problems"},
        {"label": "Total Attempts", "value": total_attempts, "subtext": "practice sessions"},
    ]

    return render(request, 'core/student_dashboard.html', {
        "stats": stats,
        "quick_practice": quick_practice,
        "recent_sessions": recent_sessions,
        "user_progress": user_progress,
        "history_page_obj": history_page_obj,
    })


@teacher_required
def teacher_dashboard_view(request):
    # Filter all queries by current teacher
    teacher_problems = Problem.objects.filter(created_by=request.user)
    
    total_problems = teacher_problems.count()
    math_problems = teacher_problems.filter(subject='Math').count()
    science_problems = teacher_problems.filter(subject='Science').count()
    
    easy_problems = teacher_problems.filter(difficulty='Easy').count()
    medium_problems = teacher_problems.filter(difficulty='Medium').count()
    hard_problems = teacher_problems.filter(difficulty='Hard').count()
    
    recent_problems = teacher_problems.order_by('-created_at')[:5]

    problem_stats = []
    for problem in teacher_problems:
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
    
    # Get unique students who attempted this teacher's problems
    total_students = ProblemProgress.objects.filter(problem__in=teacher_problems).values('student').distinct().count()
    total_attempts = ProblemProgress.objects.filter(problem__in=teacher_problems).count()
    avg_success_rate = (ProblemProgress.objects.filter(problem__in=teacher_problems, is_correct=True).count() / total_attempts * 100) if total_attempts > 0 else 0
    
    most_attempted = teacher_problems.annotate(
        attempt_count=Count('progress')
    ).order_by('-attempt_count')[:3]
    
    most_successful = teacher_problems.annotate(
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

    return render(request, 'core/teacher_dashboard.html', context)


@teacher_required
def problems_view(request):
    # Only show problems created by the current teacher
    problems = Problem.objects.filter(created_by=request.user).order_by('-created_at')

    context = {
        'problems': problems,
    }

    return render(request, 'core/problems.html', context)