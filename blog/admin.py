from django.contrib import admin
from blog.models import Post, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'description', 'is_published']
    ordering = ['updated_at']
    empty_value_display = '-empty-'
    fields = ['owner', 'title', 'description', 'text', ('approved', 'is_published')]
    list_filter = ['is_published', 'approved']
    list_per_page = 20
    search_fields = ['owner', 'title']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['username', 'post', 'text', 'is_published']
    fields = ['username', 'post', 'text', 'is_published']
    list_filter = ['is_published']
    list_per_page = 20
    search_fields = ['username', 'post']