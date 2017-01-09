from django.db.models import Q
from rest_framework.generics import ListAPIView

from hashtags.models import HashTag
from tweets.api.pagination import StandartResultsPagination
from tweets.api.serializers import TweetModelSerializer
from tweets.models import Tweet


class TagTweetAPIView(ListAPIView):
    queryset = Tweet.objects.all().order_by("-timestamp")
    serializer_class = TweetModelSerializer
    pagination_class = StandartResultsPagination

    def get_serializer_context(self):
        context = super(TagTweetAPIView, self).get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self):
        hashtag = self.kwargs.get("hashtag")
        hashtag_obj = None
        try:
            hashtag_obj = HashTag.objects.get_or_create(tag=hashtag)[0]
        except:
            pass

        if hashtag_obj:
            qs = hashtag_obj.get_tweets()
            query = self.request.GET.get("q", None)
            if query is not None:
                qs = qs.filter(
                    Q(content__icontains=query) |
                    Q(user__username__icontains=query)
                )
            return qs
        return None
