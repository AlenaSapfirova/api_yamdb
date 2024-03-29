from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and (
            request.user.is_superuser
            or request.user.is_admin
        )


class AdminOnlyPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (
                request.user.is_admin
                or request.user.is_superuser
            )
        )


class AuthorOrModerOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return (
                obj.author == request.user
                or request.user.is_admin
                or request.user.is_moderator
            )
        return False
