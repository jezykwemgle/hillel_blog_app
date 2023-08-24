from django.contrib.auth.models import User
from django.db import models
from django_lifecycle import LifecycleModel, hook


class Post(LifecycleModel):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    text = models.TextField()
    approved = models.BooleanField(default=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'

    def __str__(self):
        return self.title


class Comment(LifecycleModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE)

    text = models.TextField(max_length=100)
    is_published = models.BooleanField(default=False)


    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return self.text