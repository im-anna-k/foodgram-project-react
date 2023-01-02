from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password']

