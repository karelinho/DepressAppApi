from rest_framework import serializers
from .models import Depress
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class DepressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Depress
        fields = ('id', 'date', 'user', 'sleep', 'headache', 'tiredness', 'appetite', 'constipation',
                  'self_blame_thoughts', 'mood', 'self_destructive_thoughts', 'concentration',
                  'physical_discomfort', 'tense_feeling', 'sleep_length')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True, 'required': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        Token.objects.create(user=user)
        return user
