from django.urls import path
from .views import show_posts, create_post

urlpatterns = [
    path('', show_posts, name='show_posts'),
    path('create/', create_post, name='create_post'),
]
