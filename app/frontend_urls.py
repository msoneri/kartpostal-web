from django.urls import path, include
from django.shortcuts import redirect
from . import views

app_name = 'app'
urlpatterns = [
    path('', lambda request: redirect('feed/', permanent=False)),
    path('login/', views.login_view, name='login'),
    path('feed/', views.feed, name='feed'),
    path('post/<int:pk>/', views.post_view, name='post'),
    path('register/', views.register_view, name='register'),
    path('profile/<str:username>', views.profile_view, name='profile'),
    path('my/', views.profile_my, name='profile_my'),
    path('edit-profile/', views.edit_profile_view, name='edit_profile'),
]
