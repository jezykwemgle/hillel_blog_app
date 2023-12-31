from blog.forms import CommentForm, PostForm
from blog.models import Comment, Post
from blog.tasks import send_mail_to_admin, send_mail_to_user  # noqa

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View, generic


class HomeView(generic.TemplateView):
    """
    Головна сторінка.
    """
    template_name = 'blog/home.html'


class AllPostView(generic.ListView):
    """
    Всі опубліковані пости відсортовані за датою оновлення
    """
    model = Post
    paginate_by = 5
    template_name = 'blog/all_post_list.html'

    def get_queryset(self):
        return (super(AllPostView, self).get_queryset()
                .filter(approved=True, is_published=True)
                .select_related('owner')
                .order_by('-updated_at'))


class UserPostsView(generic.ListView):
    """
    Всі пости певного юзера, досуп за id.
    """
    model = Post
    paginate_by = 12
    template_name = 'blog/users_posts.html'

    def get_queryset(self):
        return (super(UserPostsView, self).get_queryset()
                .filter(is_published=True, approved=True, owner=self.kwargs.get('pk'))
                .select_related('owner')
                .order_by('-updated_at'))


class LoginUserPostsView(LoginRequiredMixin, generic.ListView):
    """
    Опубліковані пости залогіненого юзера (мої пости).
    """
    model = Post
    paginate_by = 12
    template_name = 'blog/my_posts.html'

    def get_queryset(self):
        return (super(LoginUserPostsView, self).get_queryset()
                .filter(is_published=True, approved=True, owner=self.request.user))


class NotPublishedLoginUserPostsView(LoginRequiredMixin, generic.ListView):
    """
    Не опубліковані пости залогіненого юзера (мої чернетки).
    """
    model = Post
    template_name = 'blog/my_drafts.html'
    paginate_by = 12

    def get_queryset(self):
        return (super(NotPublishedLoginUserPostsView, self).get_queryset()
                .filter(is_published=False, owner=self.request.user))


class PostDetailView(View):
    """
    Детальне представлення поста:
    - get -> пост, список опублікованих коментарів, пуста форма для створення нового коментаря.
    - post -> пост, список опублікованих коментарів, якщо форма валідна,
    адміну надсилається повідомлення про створення нвого коментаря.
    """
    template_name = 'blog/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(is_published=True, post=post)
        paginator = Paginator(comments, 2)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        form = CommentForm()
        return render(request, self.template_name, {'post': post, 'page_obj': page_obj, 'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        comments = Comment.objects.filter(is_published=True, post=post)
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post

            if self.request.user.is_authenticated:
                comment.owner = request.user
                send_mail_to_admin.delay(str(request.user), 'comment')
            else:
                send_mail_to_admin.delay(str('Anonymous'), 'comment')

            if self.request.user.is_superuser:
                comment.is_published = True

            # if self.request.user.username != post.owner.username:
            #     send_mail_to_user.delay(str(post.owner.username),
            #     str(post.owner.email), str(post.title),
            #     reverse_lazy('blog:post', kwargs={'pk': pk}))
            comment.save()
            return redirect('blog:post', pk=pk)

        return render(request, self.template_name, {'post': post, 'comments': comments, 'form': form})


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Створення нового поста, якщо форма валідна, адміну надсилається повідомлення про створення нового поста.
    """
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
            send_mail_to_admin.delay(str(self.request.user), 'post')
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    Оновлення поста, при оновленні і публікації оновленого поса, адміну надсилається повідомлення.
    """
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
            send_mail_to_admin.delay(str(self.request.user), 'post')
        else:
            form.instance.is_published = False
        return super().form_valid(form)


class PostDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    Видалення поста.
    """
    model = Post
    success_url = reverse_lazy('blog:users-posts')
    template_name = 'blog/post_delete.html'
