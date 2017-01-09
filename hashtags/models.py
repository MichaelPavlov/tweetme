from django.db.models import Model, CharField, DateTimeField
from django.dispatch import receiver
from django.urls import reverse_lazy

from hashtags.signals import parsed_hashtags
from tweets.models import Tweet


class HashTag(Model):
    tag = CharField(max_length=120)
    timestamp = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse_lazy("hashtag", kwargs={"hashtag": self.tag})

    def get_tweets(self):
        return Tweet.objects.filter(content__icontains='#' + self.tag)


@receiver(parsed_hashtags)
def save_hashtags(sender, hashtags, **kwargs):
    for hashtag in hashtags:
        new_tag, created = HashTag.objects.get_or_create(tag=hashtag)
