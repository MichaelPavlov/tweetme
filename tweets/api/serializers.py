from django.utils.timesince import timesince
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from accounts.api.serializers import UserDisplaySerializer
from tweets.models import Tweet


class ParentTweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    date_display = SerializerMethodField()
    timesince = SerializerMethodField()
    url = SerializerMethodField(read_only=True)
    likes = SerializerMethodField(read_only=True)
    liked = SerializerMethodField()

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'url',
            'likes',
            'liked',
        ]

    def get_likes(self, obj):
        return obj.liked_by.all().count()

    def get_liked(self, obj):
        try:
            user = self.request.user
            if user.is_authenticated() and user in obj.liked.all():
                return True
        except:
            pass
        return False

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + "ago"


class TweetModelSerializer(serializers.ModelSerializer):
    user = UserDisplaySerializer(read_only=True)
    date_display = SerializerMethodField()
    timesince = SerializerMethodField()
    url = SerializerMethodField(read_only=True)
    parent = ParentTweetModelSerializer(read_only=True)
    likes = SerializerMethodField(read_only=True)

    class Meta:
        model = Tweet
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
            'date_display',
            'timesince',
            'url',
            'parent',
            'likes',
        ]

    def get_likes(self, obj):
        return obj.liked_by.all().count()

    def get_url(self, obj):
        return obj.get_absolute_url()

    def get_date_display(self, obj):
        return obj.timestamp.strftime("%b %d %I:%M %p")

    def get_timesince(self, obj):
        return timesince(obj.timestamp) + "ago"
