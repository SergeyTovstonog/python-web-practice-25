from django.urls import path
from .views import PostListView, PostDetailView, PostCreateView, PostUpdateView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', PostListView.as_view(), name='post_list'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', PostUpdateView.as_view(), name='post_update'),
    path('post/new/', PostCreateView.as_view(), name='post_create'),  # New post creation

    # path('', post_list, name='post_list'),
    # path('post/<int:post_id>/', post_detail, name='post_detail'),

    path('login/', auth_views.LoginView.as_view(template_name="blog/login.html"), name='post_detail'),
]