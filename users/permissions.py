from rest_framework import permissions


class IsLibrarian(permissions.BasePermission):
    """Проверка прав доступа для пользователей группы librarians."""
    message = 'Вы не относитесь к группе библиотекарей'

    def has_permission(self, request, view):
        """Проверяет, состоит ли пользователь в группе librarians."""
        return request.user.groups.filter(name="librarians").exists()
