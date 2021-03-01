from django.contrib import admin
from django.urls import path
from .views import home_view, tweet_detail_view, tweet_list_view, create_tweet_view, delete_tweet_view, tweet_action_view
urlpatterns = [
    path('', tweet_list_view),
    path('create', create_tweet_view),
    path('action', tweet_action_view),
    path('<int:tweet_id>/', tweet_detail_view),
    path('<int:tweet_id>/delete/', delete_tweet_view),
    
]
