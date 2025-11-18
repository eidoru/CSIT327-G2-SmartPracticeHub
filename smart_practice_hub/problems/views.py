from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .forms import ProblemForm
from .models import Problem
from django.shortcuts import render, redirect, get_object_or_404
from .models import Problem



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

