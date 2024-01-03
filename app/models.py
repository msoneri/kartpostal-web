from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username

class Posts(models.Model):
    post_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, to_field='username', on_delete=models.CASCADE)
    post_text = models.TextField()
    image = models.ImageField(upload_to='static/post_images/', null=True, blank=True)
    post_date = models.DateTimeField(auto_now_add=True)

class Comments(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField(auto_now_add=True)

class Friends(models.Model):
    friendship_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, related_name='user_friendships', on_delete=models.CASCADE)
    friend = models.ForeignKey(CustomUser, related_name='friend_user', on_delete=models.CASCADE)
    status = models.CharField(max_length=50, default='pending')
