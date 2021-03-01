from rest_framework import serializers
from .models import Tweet
from django.conf import settings


MAX_LENGTH = settings.MAX_LENGTH
TWEET_ACTION_OPTIONS = ["like", "unlike", "retweet"]


class TweetCreateSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", "content", "likes"]

    def get_likes(self, obj):
        return obj.likes.count()

    def validate_content(self, value):
        if len(value) > MAX_LENGTH:
            raise serializers.ValidationError(
                f"This content is more than {MAX_LENGTH} characters long.")
        return value


class TweetSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField(read_only=True)
    original_tweet = TweetCreateSerializer(source="parent", read_only=True)

    class Meta:
        model = Tweet
        fields = ["id", "content", "likes", "is_retweet", "original_tweet"]

    def get_likes(self, obj):
        return obj.likes.count()


class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()

    def validate_action(self, action):
        action = action.strip().lower()
        if action not in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError(
                "This is not a valid action for tweets")
        return action
