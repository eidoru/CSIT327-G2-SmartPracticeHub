# from django.db import models
# from django.conf import settings

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import User

# class Problem(models.Model):
#     SUBJECT_CHOICES = [
#         ('Math', 'Math'),
#         ('Science', 'Science'),
#     ]


#     DIFFICULTY_CHOICES = [
#         ('Easy', 'Easy'),
#         ('Medium', 'Medium'),
#         ('Hard', 'Hard'),
#     ]

#     title = models.CharField(max_length=200)
#     subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
#     points = models.PositiveIntegerField()
#     topic = models.CharField(max_length=100)
#     difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
#     problem_text = models.TextField()
#     solution = models.TextField()
#     # created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='problems')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.title} ({self.subject})"

# class ProblemProgress(models.Model):
#     STATUS_CHOICES = [
#         ('not_started', 'Not Started'),
#         ('in_progress', 'In Progress'),
#         ('completed', 'Completed'),
#     ]

#     student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='problem_progress')
#     problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='progress')
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
#     attempts = models.PositiveIntegerField(default=0)
#     is_correct = models.BooleanField(default=False)
#     started_at = models.DateTimeField(null=True, blank=True)
#     completed_at = models.DateTimeField(null=True, blank=True)
#     last_attempted = models.DateTimeField(auto_now=True)

#     class Meta:
#         unique_together = ['student', 'problem']  # One progress record per student per problem

#     def __str__(self):
#         return f"{self.student.email} - {self.problem.title} ({self.status})"

