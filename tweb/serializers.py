from django.contrib.auth.models import User
from rest_framework import serializers

from tweb.models import Score, CustomUser


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Score
        fields = ['user', 'rating', 'time', 'initials']


class AvatarSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['user', 'avatar']