from django import forms
from django.core.exceptions import ValidationError
from .models import Problem

class ProblemForm(forms.ModelForm):
    class Meta:
        model = Problem
        fields = ['title', 'subject', 'points', 'topic', 'difficulty', 'problem_text', 'solution']
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
                'min': '1',
                'max': '1000'
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
        }
        labels = {
            'title': 'Problem Title',
            'subject': 'Subject',
            'points': 'Points',
            'topic': 'Topic',
            'difficulty': 'Difficulty',
            'problem_text': 'Problem Text',
            'solution': 'Solution',
        }
    
    def clean(self):
        """Additional validation at form level"""
        cleaned_data = super().clean()
        
        # Strip whitespace from text fields
        if 'title' in cleaned_data:
            cleaned_data['title'] = cleaned_data['title'].strip() if cleaned_data['title'] else ''
        if 'topic' in cleaned_data:
            cleaned_data['topic'] = cleaned_data['topic'].strip() if cleaned_data['topic'] else ''
        if 'problem_text' in cleaned_data:
            cleaned_data['problem_text'] = cleaned_data['problem_text'].strip() if cleaned_data['problem_text'] else ''
        if 'solution' in cleaned_data:
            cleaned_data['solution'] = cleaned_data['solution'].strip() if cleaned_data['solution'] else ''
        
        return cleaned_data
    
    def clean_title(self):
        """Validate title field"""
        title = self.cleaned_data.get('title', '').strip()
        
        if not title:
            raise ValidationError('Problem title cannot be empty.')
        
        if len(title) < 3:
            raise ValidationError('Problem title must be at least 3 characters long.')
        
        if len(title) > 200:
            raise ValidationError('Problem title cannot exceed 200 characters.')
        
        return title
    
    def clean_points(self):
        """Validate points field"""
        points = self.cleaned_data.get('points')
        
        if points is None:
            raise ValidationError('Points are required.')
        
        if points <= 0:
            raise ValidationError('Points must be a positive number.')
        
        if points > 1000:
            raise ValidationError('Points cannot exceed 1000.')
        
        return points
    
    def clean_topic(self):
        """Validate topic field"""
        topic = self.cleaned_data.get('topic', '').strip()
        
        if not topic:
            raise ValidationError('Topic cannot be empty.')
        
        if len(topic) < 2:
            raise ValidationError('Topic must be at least 2 characters long.')
        
        return topic
    
    def clean_problem_text(self):
        """Validate problem text"""
        problem_text = self.cleaned_data.get('problem_text', '').strip()
        
        if not problem_text:
            raise ValidationError('Problem text cannot be empty.')
        
        if len(problem_text) < 10:
            raise ValidationError('Problem text must be at least 10 characters long.')
        
        return problem_text
    
    def clean_solution(self):
        """Validate solution"""
        solution = self.cleaned_data.get('solution', '').strip()
        
        if not solution:
            raise ValidationError('Solution cannot be empty.')
        
        if len(solution) < 5:
            raise ValidationError('Solution must be at least 5 characters long.')
        
        return solution
        