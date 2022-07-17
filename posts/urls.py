from django.urls import path
from . import views

app_name = 'posts'
urlpatterns = [
    path('', views.create_post_comment_and_list_view, name='main-post-view'),
    path('liked/', views.like_unlike_post, name='like-post-view')
]