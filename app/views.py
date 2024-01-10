from django.shortcuts import render, redirect
from django.urls import reverse
#from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.decorators import api_view, permission_classes

from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login


from rest_framework import generics
from .models import CustomUser, Posts, Comments, Friends
from .serializers import (UsersSerializer, PostsSerializer, CommentsSerializer,
     FriendsSerializer, UserRegistrationSerializer, UserLoginSerializer, PostsSerializer, CommentsSerializer)

from rest_framework.permissions import BasePermission

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to allow only admin users to delete posts.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, and OPTIONS requests (read-only permissions)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True

        # Check if the user is an admin to allow DELETE request (deletion)
        return request.user.is_staff

@permission_classes([IsAdminUser])
class UsersListCreateAPIView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer

@permission_classes([IsAdminUser])
class UsersRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer

class PostsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

@permission_classes([IsAdminOrReadOnly])
class PostsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer

@permission_classes([AllowAny])
class CommentsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def get_queryset(self):
        post_id = self.kwargs['pk'] 
        return Comments.objects.filter(post=post_id)

class CommentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

class FriendsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

class FriendsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

@permission_classes([AllowAny])
class UserRegistrationAPIView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer

from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password

class LogoutAPIView(APIView):
    def post(self, request):
        if request.user.is_authenticated:
            # Clear the session for the authenticated user
            request.session.flush()

            return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "User is not authenticated."}, status=status.HTTP_400_BAD_REQUEST)


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('app:feed'))

    return render(request, 'app/login.html')


class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            # try:
                # user = Users.objects.get(username=username)
            # except Users.DoesNotExist:
            if user is None:
                messages.error(request, 'Invalid credentials')  # Add error message
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                login(request, user)
            # if check_password(password, user.password_hash):
                # Authentication successful
                # login(request, user)
                # messages.success(request, 'Authentication successful')  # Add success message
                return Response({'message': 'Authentication successful'}, status=status.HTTP_200_OK)
            # else:
            #     messages.error(request, 'Invalid credentials')  # Add error message
            #     return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            messages.error(request, 'Invalid format')  # Add error message for invalid data
            return Response({'message': 'Invalid format'}, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.parsers import MultiPartParser, FormParser

class PostsCreateAPIView(generics.CreateAPIView):
    queryset = Posts.objects.all()
    serializer_class = PostsSerializer
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(user=request.user)  # Assuming you are using token authentication or session authentication to identify the user
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.generics import CreateAPIView

class CreateCommentAPIView(CreateAPIView):
    serializer_class = CommentsSerializer

    def create(self, request, *args, **kwargs):
        post_id = self.kwargs.get('post_id')
        mutable_data = request.data.copy()  # Create a mutable copy of request.data
        mutable_data['post'] = post_id  # Attach the post ID to the comment data
        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def feed(request):
    # Your logic for the authenticated view
    # This will only be accessible to authenticated users
    return render(request, 'app/feed.html')

import requests
from datetime import datetime

@login_required(login_url='/login')
def post_view(request, pk):
    # Make a request to the API endpoint to get post data
    post_api_url = f'http://localhost:8000/api/posts/{pk}/'
    post_response = requests.get(post_api_url)

    if post_response.status_code == 200:
        post_data = post_response.json()

        post_date_str = post_data.get('post_date', '')
        if post_date_str.endswith('Z'):
            post_date_str = post_date_str[:-1]

        post_date = datetime.fromisoformat(post_date_str)
        formatted_date = post_date.strftime('%d/%m/%Y %H:%M')

        post_data['post_date'] = formatted_date

        # Make a request to the comments API endpoint for the specific post
        comments_api_url = f'http://localhost:8000/api/comments/{pk}/'
        comments_response = requests.get(comments_api_url)

        if comments_response.status_code == 200:
            comments_data = comments_response.json()
            comments_results = comments_data.get('results', [])
            formatted_comments = []

            for comment in comments_results:
                userid = comment.get('user', '')
                user = get_object_or_404(CustomUser, id=userid)

                comment_date_str = comment.get('comment_date', '')
                print(comment_date_str)
                if comment_date_str.endswith('Z'):
                    comment_date_str = comment_date_str[:-1]

                comment_date = datetime.fromisoformat(comment_date_str)
                formatted_date = comment_date.strftime('%d/%m/%Y %H:%M')

                comment['comment_date'] = formatted_date
                comment['username'] = user.username
                formatted_comments.append(comment)

            return render(request, 'app/post.html', {'post': post_data, 'comments': formatted_comments})


        # Pass both post and comments data to the template
        return render(request, 'app/post.html', {'post': post_data, 'comments': formatted_comments})

    # Handle error cases (404 or other status codes)
    return render(request, 'app/post.html', {'post': post_data, 'comments': None})

def register_view(request):
    return render(request, 'app/register.html')

@login_required(login_url='/login')
def profile_view(request, username):
    # Fetch user details using the provided username
    user = get_object_or_404(CustomUser, username=username)
    
    # Retrieve posts related to the user
    user_posts = Posts.objects.filter(user=user)
    
    # Pass user details and posts to the template for rendering
    return render(request, 'app/profile.html', {'user': user, 'user_posts': user_posts})


@login_required(login_url='/login')
def profile_my(request):
    user = get_object_or_404(CustomUser, username=request.user)
    return profile_view(request, user.username)

@login_required(login_url='/login')
def edit_profile_view(request):
    user = request.user  # Fetch the current logged-in user

    if request.method == 'POST':
        profile_picture = request.FILES.get('profile_picture')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        bio = request.POST.get('bio')

        # Update user profile fields
        user.profile_picture = profile_picture if profile_picture else user.profile_picture
        user.first_name = first_name if first_name else user.first_name
        user.last_name = last_name if last_name else user.last_name
        user.bio = bio if bio else user.bio

        user.save()
        messages.success(request, 'Your profile has been updated successfully.')
        return redirect('app:profile_my')  # Redirect to the profile view after successful update

    return render(request, 'app/edit_profile.html', {'user': user})