from django import forms
from .models import Problem

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'subject', 'points', 'topic', 'difficulty', 'problem_text', 'correct_answer', 'solution']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'Enter problem title'
            }),
            'subject': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'points': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'min': '1'
            }),
            'topic': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'placeholder': 'e.g., Algebra, Mechanics, etc.'
            }),
            'difficulty': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500'
            }),
            'problem_text': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 6,
                'placeholder': 'Enter the problem description...'
            }),
            'solution': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 6,
                'placeholder': 'Enter the solution...'
            }),
            'correct_answer': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500',
                'rows': 2,
                'placeholder': 'Enter the exact answer used for checking, keep it concise.'
            }),
        }
        labels = {
            'title': 'Problem Title',
            'subject': 'Subject',
            'points': 'Points',
            'topic': 'Topic',
            'difficulty': 'Difficulty',
            'problem_text': 'Problem Text',
            'correct_answer': 'Correct Answer (used for auto-check)',
            'solution': 'Solution Guide (shown to students)',
        }
        