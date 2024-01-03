from django.urls import path, include
from . import views

app_name = 'app'
urlpatterns = [
    path('login', views.login_view, name='login'),
    path('feed', views.feed, name='feed'),
    # path('post_images/<str:image_name>/', views.serve_image, name='serve_image'),

]
