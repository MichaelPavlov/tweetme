from django.db.models import Q
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from tweets.api.pagination import StandartResultsPagination
from tweets.api.serializers import TweetModelSerializer
from tweets.models import Tweet


class LikeHandler(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        tweet = get_object_or_404(Tweet, pk=pk)
        like_result = Tweet.objects.toggle_like(request.user, tweet)
        return Response({'like': like_result})


class Retweet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk, format=None):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated():
            retweet = Tweet.objects.retweet(request.user, tweet)
            data = TweetModelSerializer(retweet).data
            return Response(data, HTTP_201_CREATED)
        return Response({"message": "Bad request"}, HTTP_400_BAD_REQUEST)


class TweetCreate(CreateAPIView):
    serializer_class = TweetModelSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TweetList(ListAPIView):
    serializer_class = TweetModelSerializer
    pagination_class = StandartResultsPagination

    def get_serializer_context(self):
        context = super(TweetList, self).get_serializer_context()
        context['request'] = self.request
        return context

    def get_queryset(self, *args, **kwargs):
        requested_user = kwargs.get("username")
        if requested_user:
            qs = Tweet.objects.filter(user__username=requested_user).order_by("-timestamp")
        else:
            following = self.request.user.profile.get_following()
            qs1 = Tweet.objects.filter(user__in=following)
            qs2 = Tweet.objects.filter(user=self.request.user)
            qs = (qs1 | qs2).distinct().order_by("-timestamp")

        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs


class TweetDetail(RetrieveAPIView):
    queryset = Tweet.objects.all()
    serializer_class = TweetModelSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        tweet_id = self.kwargs.get("pk")
        qs  = Tweet.objects.filter(pk=tweet_id)
