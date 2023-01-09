from api.models import CustomUser
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'password')


class AllUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name')


class NewPassword(serializers.Serializer):
    new_password = serializers.CharField(max_length=150)
    current_password = serializers.CharField(max_length=150)
