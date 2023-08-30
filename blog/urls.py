from django.urls import path

from .views import (AllPostView, HomeView, NotPublishedUsersPostsView, PostCreateView, PostDeleteView, PostDetailView,
                    PostUpdateView, UserEditView, UserProfileView, UsersPostsView)


app_name = 'blog'
urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('all-posts/', AllPostView.as_view(), name='all-posts'),
    path('users-posts/<int:pk>/', UsersPostsView.as_view(), name='users-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post'),
    path('post/create/', PostCreateView.as_view(), name='create-post'),
    path('post/update/<int:pk>/', PostUpdateView.as_view(), name='update-post'),
    path('post/delete/<int:pk>/', PostDeleteView.as_view(), name='delete-post'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user-profile'),
    path('edit-profile/<int:pk>/', UserEditView.as_view(), name='user-edit-profile'),
    path('not-published-posts/', NotPublishedUsersPostsView.as_view(), name='not-published-posts')
]
