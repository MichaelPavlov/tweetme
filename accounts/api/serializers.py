from django.contrib.auth import get_user_model
from rest_framework.fields import SerializerMethodField
from rest_framework.reverse import reverse_lazy
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class UserDisplaySerializer(ModelSerializer):
    follower_count = SerializerMethodField()
    url = SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'follower_count',
            'url',
        ]

    def get_follower_count(self, obj):
        return 0

    def get_url(self, obj):
        return reverse_lazy("profile:detail", kwargs={"username": obj.username})
