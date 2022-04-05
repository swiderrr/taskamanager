from django import forms
from .models import Task, Comment, Picture

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        widgets = {
            'desc': forms.Textarea(attrs={'class': 'desc_area'}),
            'title': forms.TextInput(attrs={'style': 'width: 33%'}),
            'priority': forms.Select(attrs={'class': 'btn btn-secondary dropdown-toggle'}),
        }
        field = ('title', 'desc', 'priority', 'status')
        exclude = ['author', 'status', 'created_at', 'updated_at']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        widgets = {
            'text': forms.Textarea(attrs={'rows': 5, 'cols': 100, 'class': 'comment_area'}),
        }
        field = ('text')
        exclude = ['author', 'created_at', 'task']


class PictureForm(forms.ModelForm):
    class Meta:
        model = Picture
        field = ('file')
        exclude = ['comment']

    def __init__(self, *args, **kwargs):
        super(PictureForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False