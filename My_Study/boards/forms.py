from django import forms
from .models import Board, Comment

class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        # fields = '__all__'
        fields = ['title', 'content', ]

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content', ]