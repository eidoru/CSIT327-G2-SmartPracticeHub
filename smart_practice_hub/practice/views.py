from django.shortcuts import render


def practice_view(request, id):
    return render(request, 'practice/practice.html')