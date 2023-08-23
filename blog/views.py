from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import generic

from blog.models import Post


def all_posts_view(request):
        objs = (((Post.objects
                .filter(approved=True, is_published=True))
                .select_related('user'))
                .order_by('-updated_at'))
        paginator = Paginator(objs, 10)
        page = request.GET.get('page')
        page_obj = paginator.get_page(page)
        return render(request, 'blog/all_post_list.html', {'page_obj': page_obj, "is_paginated": True})


class AllPostView(generic.ListView):
    model = Post
    paginate_by = 12
    template_name = 'blog/all_post_list.html'
    def get_queryset(self):
        return (super(AllPostView, self).get_queryset()
                .filter(approved=True, is_published=True)
                .select_related('user')
                .order_by('-updated_at'))
class UsersPostsView(generic.ListView):
    ...

class PostDetailView(generic.DetailView):
    ...

class PostCreateView(generic.CreateView):
    ...

class PostUpdateView(generic.UpdateView):
    ...

class PostDeleteView(generic.DeleteView):
    ...

class CreateCommentView(generic.CreateView):
    ...
class DeleteCommentView(generic.DeleteView):
    ...