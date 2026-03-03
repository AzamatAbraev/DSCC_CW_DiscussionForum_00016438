from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import SignUpView

urlpatterns = [
	path('', views.PostListView.as_view(), name='post_list'),
	path('post/new/', views.PostCreateView.as_view(), name='post_create'),
	path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
	path('post/<slug:slug>/update/', views.PostUpdateView.as_view(), name='post_update'),
	path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
	path('logout/', auth_views.LogoutView.as_view(), name='logout'),
	path('signup/', SignUpView.as_view(), name='signup'),
  path('upvote/<slug:slug>/', views.UpvoteView, name='upvote_post'),
]