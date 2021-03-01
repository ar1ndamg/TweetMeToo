from django.test import TestCase
from .models import Tweet
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()
# Create your tests here.


class TweetTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="zxcvfdsa")
        self.userb = User.objects.create_user(
            username="testuser2", password="zxcvfdsa")
        Tweet.objects.create(content="Test Tweet 1", user=self.user)
        Tweet.objects.create(content="Test Tweet 2", user=self.user)
        Tweet.objects.create(content="Test Tweet 3", user=self.userb)

    def test_create_tweet(self):
        tweet = Tweet.objects.create(content="Test Tweet", user=self.user)
        self.assertEqual(tweet.user.username, self.user.username)

    def test_api_login(self):
        client = APIClient()
        client.login(username=self.user.username, password="zxcvfdsa")

    def test_tweet_list(self):
        client = APIClient()
        response = client.get('/api/tweets/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)

    def test_tweet_like(self):
        client = APIClient()
        client.login(username=self.user.username, password="zxcvfdsa")
        response = client.post('/api/tweets/action',
                               {"id": 1, "action": "like"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["likes"], 1)

    def test_tweet_unlike(self):
        client = APIClient()
        client.login(username=self.user.username, password="zxcvfdsa")
        response = client.post('/api/tweets/action',
                               {"id": 2, "action": "like"}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("likes"), 1)
        response = client.post('/api/tweets/action',
                               {"id": 2, "action": "unlike"}, format='json')
        self.assertEqual(response.json().get("likes"), 0)

    def test_tweet_retweet(self):
        client = APIClient()
        client.login(username=self.user.username, password="zxcvfdsa")
        response = client.post('/api/tweets/action',
                               {"id": 2, "action": "retweet"}, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json().get("is_retweet"), True)
        self.assertNotEqual(2, response.json().get("id"))

    def test_tweet_delete(self):
        client = APIClient()
        client.login(username=self.user.username, password="zxcvfdsa")
        response = client.delete('/api/tweets/3/delete/')
        self.assertEqual(response.status_code, 401)
        response = client.delete('/api/tweets/1/delete/')
        self.assertEqual(response.status_code, 200)