from django.urls import path

from .views import UserCreate, UserLogin, Logout, SetPassword, AllUsers
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('api/users/', UserCreate.as_view()),
    path('api/auth/token/login/', UserLogin.as_view()),
    path('api/auth/token/logout/', Logout.as_view()),
    path('api/users/set_password/', SetPassword.as_view()),
    path('api/users/', AllUsers.as_view()),

]
