from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from tweets.forms import TweetModelForm
from tweets.mixins import FormUserNeededMixin, UserOwnerMixin
from tweets.models import Tweet


class RetweetView(View):
    def get(self, request, pk, *args, **kwargs):
        tweet = get_object_or_404(Tweet, pk=pk)
        if request.user.is_authenticated():
            retweet = Tweet.objects.retweet(request.user, tweet)
            return HttpResponseRedirect(retweet.get_absolute_url())
        return HttpResponseRedirect(tweet.get_absolute_url())


class TweetDetailView(DetailView):
    queryset = Tweet.objects.all()


class TweetListView(ListView):
    # template_name = "tweets/tweet_list.html"

    def get_queryset(self, *args, **kwargs):
        qs = Tweet.objects.all()
        query = self.request.GET.get("q", None)
        if query is not None:
            qs = qs.filter(
                Q(content__icontains=query) |
                Q(user__username__icontains=query)
            )
        return qs

    def get_context_data(self, *args, **kwargs):
        context = super(TweetListView, self).get_context_data(**kwargs)
        context['create_form'] = TweetModelForm
        context['create_url'] = reverse_lazy('tweet-api:create')
        return context


class TweetCreateView(FormUserNeededMixin, CreateView):
    form_class = TweetModelForm
    template_name = "tweets/create_view.html"
    # success_url = '/tweet/create/'


class TweetUpdateView(LoginRequiredMixin, UserOwnerMixin, UpdateView):
    form_class = TweetModelForm
    template_name = 'tweets/update_view.html'
    # success_url = reverse_lazy("tweet:detail", kwargs={'pk': })


class TweetDeleteView(LoginRequiredMixin, DeleteView):
    model = Tweet
    template_name = "tweets/delete_confirm.html"
    success_url = reverse_lazy("tweet:list")
