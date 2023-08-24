from blog.forms import PostForm
from blog.models import Post

from django.core.paginator import Paginator  # noqa: F401
from django.shortcuts import render  # noqa: F401
from django.urls import reverse_lazy
from django.views import generic

# def all_posts_view(request):
#         objs = (((Post.objects
#                 .filter(approved=True, is_published=True))
#                 .select_related('user'))
#                 .order_by('-updated_at'))
#         paginator = Paginator(objs, 10)
#         page = request.GET.get('page')
#         page_obj = paginator.get_page(page)
#         return render(request, 'blog/all_post_list.html', {'page_obj': page_obj, "is_paginated": True})


class AllPostView(generic.ListView):
    model = Post
    paginate_by = 12
    template_name = 'blog/all_post_list.html'

    def get_queryset(self):
        return (super(AllPostView, self).get_queryset()
                .filter(approved=True, is_published=True)
                .select_related('owner')
                .order_by('-updated_at'))


class UsersPostsView(generic.ListView):
    model = Post
    paginate_by = 12
    template_name = 'blog/all_post_list.html'

    def get_queryset(self):
        return (super(UsersPostsView, self).get_queryset()
                .filter(is_published=True, owner=self.request.user.id)
                .select_related('owner')
                .order_by('-updated_at'))


class PostDetailView(generic.DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return super(PostDetailView, self).get_queryset().filter().select_related('owner')


class PostCreateView(generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class PostUpdateView(generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class PostDeleteView(generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:users-posts')
    template_name = 'blog/post_delete.html'


class CreateCommentView(generic.CreateView):
    ...


class DeleteCommentView(generic.DeleteView):
    ...
