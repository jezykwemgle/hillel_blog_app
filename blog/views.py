from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator  # noqa: F401
from django.shortcuts import get_object_or_404, redirect, render  # noqa: F401
from django.urls import reverse_lazy
from django.views import View, generic


class HomeView(generic.TemplateView):
    template_name = 'blog/home.html'


class UserProfileView(generic.DetailView):
    model = User
    template_name = 'blog/profile.html'


# TODO: зробити можливість редагування профілю тільки для юзеру який залогінився
class UserEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    template_name = 'blog/edit_profile.html'
    fields = ['username', 'email', 'first_name', 'last_name']

    def get_success_url(self):
        return reverse_lazy('blog:user-profile', kwargs={'pk': self.request.user.id})


class AllPostView(generic.ListView):
    model = Post
    paginate_by = 5
    template_name = 'blog/all_post_list.html'

    def get_queryset(self):
        return (super(AllPostView, self).get_queryset()
                .filter(approved=True, is_published=True)
                .select_related('owner')
                .order_by('-updated_at'))


class UsersPostsView(generic.ListView):
    model = Post
    paginate_by = 12
    template_name = 'blog/users_posts.html'

    def get_queryset(self):
        return (super(UsersPostsView, self).get_queryset()
                .filter(is_published=True, approved=True,  owner=self.kwargs.get('pk'))
                .select_related('owner')
                .order_by('-updated_at'))


class NotPublishedUsersPostsView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = 'blog/not_published_posts.html'
    paginate_by = 12

    def get_queryset(self):
        return (super(NotPublishedUsersPostsView, self).get_queryset()
                # TODO розібратися з аутентифікацією, треба щоб неопубліковані пости ачили тільки авторизовані
                #  користувачі і бічили тільки свої пости
                .filter(is_published=False, owner=self.request.user))


class PostDetailView(View):
    template_name = 'blog/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(is_published=True, post=post)
        form = CommentForm()
        return render(request, self.template_name, {'post': post, 'comments': comments, 'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(is_published=True, post=post)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if self.request.user.is_authenticated:
                comment.owner = request.user
            comment.save()
            return redirect('blog:post', pk=pk)
        return render(request, self.template_name, {'post': post, 'comments': comments, 'form': form})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    def get_success_url(self):
        return reverse_lazy('blog:post', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        if self.request.user.is_authenticated:
            form.instance.owner = self.request.user
        if form.instance.approved:
            form.instance.is_published = True
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Post
    success_url = reverse_lazy('blog:users-posts')
    template_name = 'blog/post_delete.html'
