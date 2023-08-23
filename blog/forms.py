from django import forms

from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['owner', 'title', 'description', 'text', 'approved']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['username', 'post', 'text']