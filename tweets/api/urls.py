from django.conf.urls import url

from tweets.api.views import TweetList, TweetCreate, Retweet, TweetDetail, LikeHandler

urlpatterns = [
    url(r'^$', TweetList.as_view(), name='list'),
    url(r'^create/$', TweetCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/retweet/$', Retweet.as_view(), name='retweet'),
    url(r'^(?P<pk>\d+)/like/$', LikeHandler.as_view(), name='like'),
    url(r'^(?P<pk>\d+)/$', TweetDetail.as_view(), name='detail'),
]
