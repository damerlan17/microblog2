from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.PostListView.as_view(), name='home'),
    # path('register/', views.RegisterView.as_view(), name='register'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    # path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    # path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    # path('profile/delete/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    # path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    # path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    # path('post/<int:pk>/like/', views.like_post, name='like_post'),
    # path('post/<int:pk>/comment/', views.add_comment, name='add_comment'),
    # path('comment/<int:pk>/edit/', views.CommentUpdateView.as_view(), name='comment_edit'),
    # path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='comment_delete'),
]