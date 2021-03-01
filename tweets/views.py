from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from django.utils.http import is_safe_url
from django.conf import settings
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
from random import randint

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request, *args, **kwargs):
    return render(request, "pages/home.html", context={}, status=200)


@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    qs = Tweet.objects.all()
    serializer = TweetSerializer(qs, many=True)
    return Response(serializer.data, status=200)


@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    tweets = Tweet.objects.filter(id=tweet_id)
    if not tweets.exists():
        return Response({}, status=404)
    tweet = tweets.first()
    serializer = TweetSerializer(tweet)
    return Response(serializer.data, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def create_tweet_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.POST)
    print("Create called with: ", request.POST["content"])
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        print("Serializer: ", serializer.data)
        return Response(serializer.data, status=201)
    return Response({}, status=400)


@api_view(['DELETE', 'POST'])
@permission_classes([IsAuthenticated])
def delete_tweet_view(request, tweet_id, *args, **kwargs):
    tweets = Tweet.objects.filter(id=tweet_id)
    if not tweets.exists():
        return Response({}, status=404)
    tweets = tweets.filter(user=request.user)
    if not tweets.exists():
        return Response({"message": "You can not delete this tweet."}, status=401)
    tweet = tweets.first()
    tweet.delete()
    return Response({'message': 'Tweet has been deleted.'}, status=200)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    """
    id is required
    actions: like, unlike, retweet
    """
    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        data = serializer.validated_data
        tweet_id = data.get('id')
        action = data.get('action')
        content = data.get('content')
        tweets = Tweet.objects.filter(id=tweet_id)
        if not tweets.exists():
            return Response({}, status=404)
        tweet = tweets.first()
        if action == 'like':
            tweet.likes.add(request.user)
            serializer = TweetSerializer(tweet)
            return Response(serializer.data, status=200)
        elif action == 'unlike':
            tweet.likes.remove(request.user)
            serializer = TweetSerializer(tweet)
            return Response(serializer.data, status=200)
        elif action == 'retweet':
            parent_tweet = tweet
            new_tweet = Tweet.objects.create(
                parent=parent_tweet, user=request.user, content=content)
            serializer = TweetSerializer(new_tweet)
            return Response(serializer.data, status=201)
