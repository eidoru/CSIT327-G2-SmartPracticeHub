from django.db import models
from django.conf import settings

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

    class Meta:
        unique_together = ['title', 'subject', 'topic']
        indexes = [
            models.Index(fields=['subject', 'difficulty']),
            models.Index(fields=['topic']),
        ]

    def __str__(self):
        return f"{self.title} ({self.subject})"
    
    def clean(self):
        """Validate problem data before saving"""
        from django.core.exceptions import ValidationError
        
        # Check for empty fields
        if not self.title or not self.title.strip():
            raise ValidationError({'title': 'Problem title cannot be empty.'})
        
        if not self.problem_text or not self.problem_text.strip():
            raise ValidationError({'problem_text': 'Problem text cannot be empty.'})
        
        if not self.solution or not self.solution.strip():
            raise ValidationError({'solution': 'Solution cannot be empty.'})
        
        if not self.topic or not self.topic.strip():
            raise ValidationError({'topic': 'Topic cannot be empty.'})
        
        # Validate points
        if self.points <= 0:
            raise ValidationError({'points': 'Points must be a positive number.'})
        
        if self.points > 1000:
            raise ValidationError({'points': 'Points cannot exceed 1000.'})
        
        # Check for duplicate based on title, subject, and topic
        duplicate = Problem.objects.filter(
            title__iexact=self.title.strip(),
            subject=self.subject,
            topic__iexact=self.topic.strip()
        ).exclude(pk=self.pk)
        
        if duplicate.exists():
            raise ValidationError(
                f'A problem with the title "{self.title}" already exists for {self.subject} - {self.topic}. '
                'Please use a different title or modify the topic.'
            )
    
    def save(self, *args, **kwargs):
        """Clean data before saving"""
        self.clean()
        # Strip whitespace from text fields
        self.title = self.title.strip() if self.title else ''
        self.topic = self.topic.strip() if self.topic else ''
        self.problem_text = self.problem_text.strip() if self.problem_text else ''
        self.solution = self.solution.strip() if self.solution else ''
        super().save(*args, **kwargs)

# Add this to your models.py file
class ProblemProgress(models.Model):
    """Track student progress on individual problems"""
    
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='problem_progress'
    )
    problem = models.ForeignKey(
        'Problem',
        on_delete=models.CASCADE,
        related_name='progress'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_started'
    )
    attempts = models.IntegerField(default=0)
    is_correct = models.BooleanField(default=False)
    student_answer = models.TextField(blank=True, null=True)
    first_attempted_at = models.DateTimeField(auto_now_add=True)
    last_attempted_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    time_spent = models.IntegerField(default=0, help_text="Time spent in seconds")
    
    class Meta:
        unique_together = ['student', 'problem']
        ordering = ['-last_attempted_at']
        verbose_name = 'Problem Progress'
        verbose_name_plural = 'Problem Progress'
    
    def __str__(self):
        return f"{self.student.username} - {self.problem.title} ({self.status})"
    
    def mark_correct(self):
        """Mark this problem as correctly solved"""
        from django.utils import timezone
        self.is_correct = True
        self.status = 'completed'
        if not self.completed_at:
            self.completed_at = timezone.now()
        self.save()


class PracticeSession(models.Model):
    """Track practice sessions for analytics"""
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='practice_sessions'
    )
    problem = models.ForeignKey(
        'Problem',
        on_delete=models.CASCADE,
        related_name='practice_sessions'
    )
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    was_correct = models.BooleanField(default=False)
    answer_given = models.TextField(blank=True, null=True)
    
    class Meta:
        ordering = ['-started_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.started_at.strftime('%Y-%m-%d %H:%M')}"