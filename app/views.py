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
     FriendsSerializer, UserRegistrationSerializer, UserLoginSerializer, PostsSerializer)

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

class CommentsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

class CommentsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

class FriendsListCreateAPIView(generics.ListCreateAPIView):
    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

class FriendsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Friends.objects.all()
    serializer_class = FriendsSerializer

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

from django.contrib.auth.decorators import login_required

@login_required(login_url='/login')
def feed(request):
    # Your logic for the authenticated view
    # This will only be accessible to authenticated users
    return render(request, 'app/feed.html')

import os.path
from django.conf import settings

# def serve_image(request, image_name):
#     # Directory path where your images are stored
#     image_directory = os.path.join(settings.BASE_DIR, 'post_images')

#     # Path of the requested image
#     image_path = os.path.join(image_directory, image_name)

#     # Check if the requested file exists
#     if os.path.exists(image_path):
#         # Open the file in binary mode and serve it as HttpResponse
#         with open(image_path, 'rb') as file:
#             return Response(file.read(), content_type='image/png')
#     else:
#         raise Http404("Image does not exist")
