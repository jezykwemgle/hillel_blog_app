from django.urls import path

from .views import AllPostView, PostCreateView, PostDeleteView, PostDetailView, PostUpdateView, UsersPostsView, HomeView


app_name = 'blog'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('all-posts/', AllPostView.as_view(), name='all-posts'),
    path('users-posts/', UsersPostsView.as_view(), name='users-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='create-post'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='update-post'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='delete-post'),
]
