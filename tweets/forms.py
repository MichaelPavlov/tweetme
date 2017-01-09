from django.forms import CharField
from django.forms import ModelForm
from django.forms import Textarea

from tweets.models import Tweet


class TweetModelForm(ModelForm):
    content = CharField(label='', widget=Textarea(attrs={'placeholder': "Your message", "class": "form-control"}))

    class Meta:
        model = Tweet
        fields = [
            'content',
        ]
