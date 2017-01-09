from django.conf.urls import url

from tweets.views import TweetListView, TweetDetailView, TweetCreateView, TweetUpdateView, TweetDeleteView, RetweetView

urlpatterns = [
    url(r'^search/$', TweetListView.as_view(), name='list'),
    url(r'^create/$', TweetCreateView.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', TweetDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/retweet/$', RetweetView.as_view(), name='retweet'),
    url(r'^(?P<pk>\d+)/update/$', TweetUpdateView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', TweetDeleteView.as_view(), name='delete'),
]
