from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdmin(BasePermission):
    """Проверка на администратора."""
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and request.user.is_admin) or request.user.is_superuser


class IsModerator(BasePermission):
    """Проверка на модератора."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator


class IsAdminOrReadOnly(BasePermission):
    """Права только администратора, для остальных только чтение."""
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and request.user.is_admin
            or request.method in SAFE_METHODS
        )


class IsAuthorAdminModeratorOrReadOnly(BasePermission):
    """
    Права только у автора, администратора, модератора,
    для остальных только чтение.
    """
    def has_object_permission(self, request, view, obj):
        return (
            request.method in 'GET'
            or request.user == obj.author
            or request.user.is_moderator or request.user.is_admin
            or request.user.is_superuser
        )
