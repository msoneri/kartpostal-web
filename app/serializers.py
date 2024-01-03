from rest_framework import serializers
from .models import CustomUser, Posts, Comments, Friends

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'

class FriendsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friends
        fields = '__all__'

from django.contrib.auth.hashers import make_password, check_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password')

    def create(self, validated_data):
        # Hash the password before saving the user
        hashed_password = make_password(validated_data['password'])

        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            password=hashed_password  # Save the hashed password
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class PostsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Posts
        fields = ('post_id', 'user', 'post_text', 'image', 'post_date')

    def create(self, validated_data):
        # 'user' is extracted from request context or authenticated user
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)
