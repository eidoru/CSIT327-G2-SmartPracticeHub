from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    SUBJECT_CHOICES = [
        ('Math', 'Math'),
        ('Science', 'Science'),
    ]

    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]

    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES)
    points = models.PositiveIntegerField()
    topic = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    problem_text = models.TextField()
    solution = models.TextField()
    # created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='problems')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.subject})"

