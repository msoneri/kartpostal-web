from django.urls import path, include
from . import views
from rest_framework import routers

urlpatterns = [
    # path('login', views.login, name='login'),
    # Users endpoints
    path('users/', views.UsersListCreateAPIView.as_view(), name='users-list'),
    path('users/<int:pk>/', views.UsersRetrieveUpdateDestroyAPIView.as_view(), name='users-detail'),
    
    # Posts endpoints
    path('posts/', views.PostsListCreateAPIView.as_view(), name='posts-list'),
    path('posts/<int:pk>/', views.PostsRetrieveUpdateDestroyAPIView.as_view(), name='posts-detail'),
    
    # Comments endpoints
    path('comments/', views.CommentsListCreateAPIView.as_view(), name='comments-list'),
    path('comments/<int:pk>/', views.CommentsRetrieveUpdateDestroyAPIView.as_view(), name='comments-detail'),
    
    # Friends endpoints
    path('friends/', views.FriendsListCreateAPIView.as_view(), name='friends-list'),
    path('friends/<int:pk>/', views.FriendsRetrieveUpdateDestroyAPIView.as_view(), name='friends-detail'),

    path('register/', views.UserRegistrationAPIView.as_view(), name='user-register'),
    path('login/', views.UserLoginAPIView.as_view(), name='user-login'),
    path('logout/', views.LogoutAPIView.as_view(), name='api-logout'),
    
    path('posts/create/', views.PostsCreateAPIView.as_view(), name='posts-create'),

]
