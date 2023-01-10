from django.urls import path

from .views import (
    AllUsers,
    GetMe,
    Logout,
    SetPassword,
    UserCreate,
    UserGetId,
    UserLogin,
)

urlpatterns = [
    path("api/users/", UserCreate.as_view()),
    path("api/auth/token/login/", UserLogin.as_view()),
    path("api/auth/token/logout/", Logout.as_view()),
    path("api/users/<int:id>/", UserGetId.as_view()),
    path("api/users/me/", GetMe.as_view()),
    path("api/users/set_password/", SetPassword.as_view()),
    path("api/users/", AllUsers.as_view()),
]
