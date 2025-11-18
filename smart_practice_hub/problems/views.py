from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db.models import Count, Avg
import json

from django.utils import timezone
from .models import Problem, ProblemProgress, PracticeSession
from .forms import ProblemForm
from django.shortcuts import render, redirect, get_object_or_404



# ----------------------------------------------------
# Regular form view (unchanged)
# ----------------------------------------------------
@login_required
def add_problem(request):
    if request.user.role != 'teacher':
        raise PermissionDenied("Only teachers can add problems.")
    
    if request.method == 'POST':
        form = ProblemForm(request.POST)
        if form.is_valid():
            try:
                problem = form.save()
                messages.success(request, f'Problem "{problem.title}" created successfully!')
                return redirect('add_problem')
            except Exception as e:
                messages.error(request, f'Error creating problem: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProblemForm()
    
    return render(request, 'problems/add_problem.html', {'form': form})


# ----------------------------------------------------
# API: Create Problem
# /api/problems/create
# ----------------------------------------------------
@csrf_exempt
@require_http_methods(["POST"])
def create_problem_api(request):
    try:
        data = json.loads(request.body) if request.content_type == 'application/json' else request.POST.dict()

        required_fields = ['title', 'subject', 'points', 'topic', 'difficulty', 'problem_text', 'solution']
        missing = [f for f in required_fields if not data.get(f)]

        if missing:
            return JsonResponse({
                'success': False,
                'message': f'Missing fields: {", ".join(missing)}',
                'errors': {f: 'Required' for f in missing}
            }, status=400)

        # validate
        if data['subject'] not in [c[0] for c in Problem.SUBJECT_CHOICES]:
            return JsonResponse({'success': False, 'message': 'Invalid subject'}, status=400)

        if data['difficulty'] not in [c[0] for c in Problem.DIFFICULTY_CHOICES]:
            return JsonResponse({'success': False, 'message': 'Invalid difficulty'}, status=400)

        try:
            points = int(data['points'])
            if points <= 0:
                raise ValueError
        except:
            return JsonResponse({'success': False, 'message': 'Points must be a positive number'}, status=400)

        problem = Problem.objects.create(
            title=data['title'],
            subject=data['subject'],
            points=points,
            topic=data['topic'],
            difficulty=data['difficulty'],
            problem_text=data['problem_text'],
            solution=data['solution']
        )

        return JsonResponse({
            'success': True,
            'message': 'Problem created successfully',
            'problem_id': problem.id
        }, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)



# ----------------------------------------------------
# API: Update Problem
# /api/problems/<id>/update
# ----------------------------------------------------
@csrf_exempt
@require_http_methods(["PUT", "PATCH"])
def update_problem_api(request, id):
    try:
        try:
            problem = Problem.objects.get(id=id)
        except Problem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Problem not found'}, status=404)

        data = json.loads(request.body)

        # Only update fields that were provided
        for field in ['title', 'subject', 'points', 'topic', 'difficulty', 'problem_text', 'solution']:
            if field in data:
                if field == "points":
                    try:
                        data[field] = int(data[field])
                        if data[field] <= 0:
                            raise ValueError
                    except:
                        return JsonResponse({'success': False, 'message': 'Points must be a positive number'}, status=400)

                setattr(problem, field, data[field])

        problem.save()

        return JsonResponse({
            'success': True,
            'message': 'Problem updated successfully',
            'problem_id': problem.id
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)



# ----------------------------------------------------
# API: Delete Problem
# /api/problems/<id>/delete
# ----------------------------------------------------
@csrf_exempt
@require_http_methods(["DELETE"])
def delete_problem_api(request, id):
    try:
        try:
            problem = Problem.objects.get(id=id)
        except Problem.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Problem not found'}, status=404)

        problem.delete()
        return JsonResponse({'success': True, 'message': 'Problem deleted successfully'})

    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, status=500)

        from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


@login_required
def update_problem(request, id):
    # Only teachers can edit
    if request.user.role != 'teacher':
        raise PermissionDenied("Only teachers can edit problems.")

    problem = get_object_or_404(Problem, id=id)

    if request.method == "POST":
        form = ProblemForm(request.POST, instance=problem)
        if form.is_valid():
            form.save()
            messages.success(request, f'Problem "{problem.title}" updated successfully!')
            return redirect('teacher_dashboard')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProblemForm(instance=problem)

    return render(request, "problems/edit_problem.html", {
        "form": form,
        "problem": problem
    })


@login_required
def delete_problem(request, id):
    # Only teachers can delete
    if request.user.role != 'teacher':
        raise PermissionDenied("Only teachers can delete problems.")

    problem = get_object_or_404(Problem, id=id)

    if request.method == "POST":
        problem.delete()
        messages.success(request, "Problem deleted successfully!")
        return redirect('teacher_dashboard')

    # If someone tries to GET this URL
    return redirect('teacher_dashboard')

#Answering Problems
@login_required
def answer_problem(request, id):
    problem = get_object_or_404(Problem, id=id)
    
    context = {
        "problem": problem,
        "student_answer": "",
        "show_solution": False
    }

    if request.method == "POST":
        # Check if user wants to see solution
        if request.POST.get("show_solution"):
            context["show_solution"] = True
            messages.info(request, "Here's the solution for reference.")
            return render(request, "problems/answer_problem.html", context)
        
        # Normal answer submission
        student_answer = request.POST.get("answer", "")
        context["student_answer"] = student_answer

        # Compare answer (case-insensitive and stripped)
        is_correct = student_answer.strip().lower() == problem.solution.strip().lower()

        # Get or create ProblemProgress record
        progress, created = ProblemProgress.objects.get_or_create(
            student=request.user,
            problem=problem
        )
        
        # Update progress
        progress.student_answer = student_answer
        progress.is_correct = is_correct
        progress.attempts += 1
        progress.status = 'completed' if is_correct else 'in_progress'
        
        if is_correct:
            from django.utils import timezone
            progress.completed_at = timezone.now()
        
        progress.save()
        
        # Create a PracticeSession record
        PracticeSession.objects.create(
            user=request.user,
            problem=problem,
            was_correct=is_correct,
            answer_given=student_answer
        )

        if is_correct:
            messages.success(request, "Correct! 🎉 Great job!")
        else:
            messages.error(request, "Incorrect ❌ Try again!")

        return render(request, "problems/answer_problem.html", context)

    return render(request, "problems/answer_problem.html", context)


@login_required
def my_progress(request):
    """Display user's practice progress and statistics"""
    
    user = request.user
    
    # Get all progress records for this user
    user_progress = ProblemProgress.objects.filter(
        student=user
    ).select_related('problem').order_by('-last_attempted_at')
    
    # Calculate statistics
    total_attempted = user_progress.count()
    total_completed = user_progress.filter(status='completed', is_correct=True).count()
    in_progress = user_progress.filter(status='in_progress').count()
    total_problems = Problem.objects.count()
    
    # Calculate completion percentage
    completion_percentage = (total_completed / total_problems * 100) if total_problems > 0 else 0
    
    # Calculate total points earned
    completed_problems = user_progress.filter(is_correct=True).select_related('problem')
    total_points = sum(p.problem.points for p in completed_problems)
    
    # Get subject-wise breakdown
    subject_stats = user_progress.filter(is_correct=True).values(
        'problem__subject'
    ).annotate(
        count=Count('id')
    ).order_by('-count')
    
    # Calculate average attempts
    avg_attempts = user_progress.aggregate(
        avg=Avg('attempts')
    )['avg'] or 0
    
    # Stats cards data
    stats = [
        {
            'label': 'Problems Solved',
            'value': total_completed,
            'subtext': f'{completion_percentage:.1f}% of all problems'
        },
        {
            'label': 'Total Points',
            'value': total_points,
            'subtext': 'Points earned'
        },
        {
            'label': 'In Progress',
            'value': in_progress,
            'subtext': 'Problems attempted'
        },
        {
            'label': 'Average Attempts',
            'value': f'{avg_attempts:.1f}',
            'subtext': 'Per problem'
        }
    ]
    
    # Quick practice suggestions - subjects with available problems
    quick_practice = []
    for subject, _ in Problem.SUBJECT_CHOICES:
        problems_count = Problem.objects.filter(subject=subject).count()
        solved_count = user_progress.filter(
            problem__subject=subject,
            is_correct=True
        ).count()
        
        last_practiced = user_progress.filter(
            problem__subject=subject
        ).order_by('-last_attempted_at').first()
        
        if problems_count > 0:
            quick_practice.append({
                'name': subject,
                'problem_count': problems_count - solved_count,
                'last_practiced': last_practiced.last_attempted_at.strftime('%b %d, %Y') if last_practiced else 'Never'
            })
    
    # Recent activity - last 10 practice sessions
    recent_sessions = PracticeSession.objects.filter(
        user=user
    ).select_related('problem').order_by('-started_at')[:10]
    
    context = {
        'stats': stats,
        'user_progress': user_progress[:10],  # Show last 10
        'quick_practice': quick_practice,
        'recent_sessions': recent_sessions,
        'subject_stats': subject_stats,
    }
    
    return render(request, 'my_progress.html', context)