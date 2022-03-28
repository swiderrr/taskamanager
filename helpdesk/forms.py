from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        field = ('title', 'desc', 'priority', 'status')
        exclude = ['author', 'status', 'created_at', 'updated_at']

