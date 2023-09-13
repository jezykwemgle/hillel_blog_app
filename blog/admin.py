from blog.models import Comment, Post
from blog.tasks import send_mail_to_user

from django.contrib import admin
from django.urls import reverse_lazy


class CommentInline(admin.StackedInline):
    model = Comment
    extra = 3


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['owner', 'title', 'description', 'is_published']
    ordering = ['updated_at']
    empty_value_display = '-empty-'
    fields = ['owner', 'title', 'description', 'text', ('approved', 'is_published')]
    list_filter = ['is_published', 'approved']
    list_per_page = 20
    search_fields = ['owner', 'title']
    inlines = [CommentInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['owner', 'post', 'text', 'is_published']
    fields = ['owner', 'post', 'text', 'is_published']
    list_filter = ['is_published']
    list_per_page = 20
    search_fields = ['owner', 'post']
    actions = ['make_approved']

    @admin.action(description='Make selected comments approved')
    def make_approved(self, request, queryset):
        queryset.update(is_published=True)
        for c in queryset:
            send_mail_to_user.delay(str(c.owner), str(c.owner.email), str(c.post.title),
                                    reverse_lazy('blog:post', kwargs={'pk': c.post.pk}))
