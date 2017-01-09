import re

from django.conf import settings
from django.db import models
from django.db.models import ForeignKey
from django.db.models import Manager
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from hashtags.signals import parsed_hashtags


class TweetManager(Manager):
    def retweet(self, user, tweet):
        if tweet.parent:
            original_tweet = tweet.parent
        else:
            original_tweet = tweet
        qs = self.filter(
            user=user, parent=original_tweet
        ).filter(
            timestamp__year=timezone.now().year,
            timestamp__month=timezone.now().month,
            timestamp__day=timezone.now().day
        )
        if qs.exists():
            return None

        obj = self.model(
            parent=tweet,
            user=user,
            content=tweet.content
        )
        obj.save()
        return obj

    def toggle_like(self, user, tweet):
        if user in tweet.liked_by.all():
            like = False
            tweet.liked_by.remove(user)
        else:
            like = True
            tweet.liked_by.add(user)

        return like


class Tweet(models.Model):
    parent = ForeignKey("self", blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    content = models.CharField(max_length=140)
    liked_by = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='liked')
    is_reply = models.BooleanField(verbose_name='Is a reply?', default=False)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = TweetManager()

    class Meta:
        ordering = ['-timestamp', 'content']

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse("tweet:detail", kwargs={'pk': self.pk})

    def get_parent(self):
        return self.parent or self

    def get_children(self):
        parent = self.get_parent()
        return Tweet.objects.filter(Q(parent=parent) | Q(pk=parent.pk))


@receiver(post_save, sender=Tweet)
def tweet_post_save(sender, instance, created, *args, **kwargs):
    if created and not instance.parent:
        username_regex = r'@(?P<username>[\w.@+-]+)'
        usernames = re.findall(username_regex, instance.content)
        # send notifications to users

        hash_regex = r'#(?P<hashtag>[\w\d-]+)'
        hashtags = re.findall(hash_regex, instance.content)
        parsed_hashtags.send(sender, hashtags=hashtags)
