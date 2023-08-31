from django.urls import path

from .views import (AllPostView, HomeView, LoginUserPostsView, NotPublishedLoginUserPostsView, PostCreateView,
                    PostDeleteView, PostDetailView, PostUpdateView, UserPostsView)

app_name = 'blog'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('all-posts/', AllPostView.as_view(), name='all-posts'),
    path('my-posts/', LoginUserPostsView.as_view(), name='my-posts'),
    path('users-posts/<int:pk>/', UserPostsView.as_view(), name='users-posts'),
    path('my-drafts/', NotPublishedLoginUserPostsView.as_view(), name='my-drafts'),


    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='create-post'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='update-post'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='delete-post'),
]
