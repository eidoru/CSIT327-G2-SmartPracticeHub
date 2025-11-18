# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from django.views.decorators.http import require_http_methods
# import json
# from .forms import ProblemForm
# from .models import Problem

# # Regular form view
# @login_required
# def add_problem(request):
#     # Check if user is a teacher
#     if request.user.role != 'teacher':
#         raise PermissionDenied("Only teachers can add problems.")
    
#     if request.method == 'POST':
#         form = ProblemForm(request.POST)
#         if form.is_valid():
#             try:
#                 problem = form.save()
#                 messages.success(request, f'Problem "{problem.title}" created successfully!')
#                 return redirect('add_problem')
#             except Exception as e:
#                 messages.error(request, f'Error creating problem: {str(e)}')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = ProblemForm()
    
#     return render(request, 'problems/add_problem.html', {'form': form})

# # API Endpoint
# @csrf_exempt
# @require_http_methods(["POST"])
# def create_problem_api(request):
#     """
#     API endpoint: /api/problems/create
#     Creates a new problem and validates subject and difficulty fields.
#     """
#     try:
#         # Parse JSON data if Content-Type is application/json
#         if request.content_type == 'application/json':
#             data = json.loads(request.body)
#         else:
#             # Handle form data
#             data = request.POST.dict()
        
#         # Validate required fields
#         required_fields = ['title', 'subject', 'points', 'topic', 'difficulty', 'problem_text', 'solution']
#         missing_fields = [field for field in required_fields if not data.get(field)]
        
#         if missing_fields:
#             return JsonResponse({
#                 'success': False,
#                 'message': f'Missing required fields: {", ".join(missing_fields)}',
#                 'errors': {field: 'This field is required.' for field in missing_fields}
#             }, status=400)
        
#         # Validate subject
#         valid_subjects = [choice[0] for choice in Problem.SUBJECT_CHOICES]
#         if data.get('subject') not in valid_subjects:
#             return JsonResponse({
#                 'success': False,
#                 'message': f'Invalid subject. Must be one of: {", ".join(valid_subjects)}',
#                 'errors': {'subject': f'Invalid subject. Must be one of: {", ".join(valid_subjects)}'}
#             }, status=400)
        
#         # Validate difficulty
#         valid_difficulties = [choice[0] for choice in Problem.DIFFICULTY_CHOICES]
#         if data.get('difficulty') not in valid_difficulties:
#             return JsonResponse({
#                 'success': False,
#                 'message': f'Invalid difficulty. Must be one of: {", ".join(valid_difficulties)}',
#                 'errors': {'difficulty': f'Invalid difficulty. Must be one of: {", ".join(valid_difficulties)}'}
#             }, status=400)
        
#         # Validate points (must be positive integer)
#         try:
#             points = int(data.get('points'))
#             if points <= 0:
#                 raise ValueError("Points must be positive")
#         except (ValueError, TypeError):
#             return JsonResponse({
#                 'success': False,
#                 'message': 'Points must be a positive integer',
#                 'errors': {'points': 'Points must be a positive integer'}
#             }, status=400)
        
#         # Create the problem
#         problem = Problem.objects.create(
#             title=data.get('title'),
#             subject=data.get('subject'),
#             points=points,
#             topic=data.get('topic'),
#             difficulty=data.get('difficulty'),
#             problem_text=data.get('problem_text'),
#             solution=data.get('solution')
#         )
        
#         return JsonResponse({
#             'success': True,
#             'message': f'Problem "{problem.title}" created successfully!',
#             'problem_id': problem.id,
#             'data': {
#                 'id': problem.id,
#                 'title': problem.title,
#                 'subject': problem.subject,
#                 'points': problem.points,
#                 'topic': problem.topic,
#                 'difficulty': problem.difficulty,
#                 'created_at': problem.created_at.isoformat()
#             }
#         }, status=201)
        
#     except json.JSONDecodeError:
#         return JsonResponse({
#             'success': False,
#             'message': 'Invalid JSON format'
#         }, status=400)
#     except Exception as e:
#         return JsonResponse({
#             'success': False,
#             'message': f'Error creating problem: {str(e)}'
#         }, status=500)
