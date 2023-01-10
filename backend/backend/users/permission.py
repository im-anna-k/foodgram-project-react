from rest_framework.permissions import BasePermission


class IsNotAuth(BasePermission):
    """
    Пермишен пускает только Автора или Администратора.
    Для остальных доступ только на чтение.
    """

    def has_permission(self, request, view):
        return bool(not request.user.is_authenticated)
