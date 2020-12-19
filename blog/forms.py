# Custom form for Blog App

from .models import Comment, Post
from django import forms
from django_summernote.widgets import SummernoteWidget


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    class Meta:
        model = Post
        fields = ['title', 'category', 'thumbnail', 'excerpt', 'content', 'featured', 'status']


class DashboardForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['featured']
