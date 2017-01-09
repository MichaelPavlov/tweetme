from django.contrib import admin

from tweets.forms import TweetModelForm
from tweets.models import Tweet


class TweetModelAdmin(admin.ModelAdmin):
    form = TweetModelForm

    class Meta:
        model = Tweet


admin.site.register(Tweet, TweetModelAdmin)
