from django.contrib.auth import authenticate
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .permission import IsNotAuth
from .serialize import UserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from api.models import CustomUser


class UserCreate(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsNotAuth]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            user = CustomUser.objects.create_user(
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password')
            )
            user.username = serializer.validated_data.get('username')
            user.last_name = serializer.validated_data.get('last_name')
            user.first_name = serializer.validated_data.get('first_name')
            user.save()
            user = CustomUser.objects.get(email=serializer.validated_data.get('email'))
            data = {
                'email': user.email,
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
            return Response(status=status.HTTP_201_CREATED, data=data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class UserLogin(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsNotAuth]

    def post(self, request, *args, **kwargs):
        username = request.data.get('email')
        password = request.data.get('password')
        if username and password:
            user = authenticate(
                request=request,
                username=username, password=password
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SetPassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user



class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)
