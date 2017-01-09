from django.conf.urls import url

from tweets.api.views import TweetList

urlpatterns = [
    url(r'^(?P<username>[\w.@+-]+)/tweet/$', TweetList.as_view(), name='tweets'),
]
