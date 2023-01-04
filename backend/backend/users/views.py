from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from .permission import IsNotAuth
from .serialize import UserSerializer, NewPassword, AllUserSerializer
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from api.models import CustomUser, SubscribingAuthors


class UserCreate(APIView):
    serializer_class = UserSerializer

    # permission_classes = [IsNotAuth]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = CustomUser.objects.create_user(
                email=serializer.validated_data.get('email'),
                password=serializer.validated_data.get('password'),
                username=serializer.validated_data.get('username'),
                last_name=serializer.validated_data.get('last_name'),
                first_name=serializer.validated_data.get('first_name'),
            )

            SubscribingAuthors.objects.create(
                user=user
            )
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

    def get(self, request, *args, **kwargs):
        data = []
        if request.user.is_authenticated is not False:
            subscribing_authors = SubscribingAuthors.objects.get(user=request.user).subscribing_authors
        else:
            subscribing_authors = None
        for user in CustomUser.objects.all():
            if subscribing_authors is not None and user in subscribing_authors.all():
                temp = True
            else:
                temp = False
            data.append(
                {
                    'email': user.email,
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'is_subscribed': temp
                }
            )
        return Response(data=data, status=status.HTTP_200_OK)


class UserLogin(APIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsNotAuth]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')
        if email and password:
            user = authenticate(
                request=request,
                email=email, password=password
            )
            if user:
                token, created = Token.objects.get_or_create(user=user)

                return Response({'token': token.key}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class SetPassword(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NewPassword(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.validated_data.get('current_password')):
                user.set_password(serializer.validated_data.get('new_password'))
                user.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED,
                                data={
                                    "detail": "Учетные данные не были предоставлены."
                                })
        return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


class AllUsers(ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = AllUserSerializer
