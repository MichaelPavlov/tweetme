from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from tweets.models import Tweet

User = get_user_model()


class TweetModelTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='Pacman')

    def test_tweet_item(self):
        obj = Tweet.objects.create(
            user=self.user1,
            content='Some random content'
        )
        self.assertTrue(obj.content == 'Some random content')
        obj_url = reverse("tweet:detail", kwargs={'pk': obj.pk})
        self.assertEqual(obj.get_absolute_url(), obj_url)

    def test_tweet_url(self):
        obj = Tweet.objects.create(user=User.objects.first(), content='Django tests are dumb but helpfull')
        absolute_url = reverse("tweet:detail", kwargs={"pk": obj.pk})
        self.assertEqual(obj.get_absolute_url(), absolute_url)
