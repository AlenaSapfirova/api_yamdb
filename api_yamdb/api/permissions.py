
from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS
)


class IsAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False

# from rest_framework import permissions import (
#     BasePermission,
#     SAFE_METHODS
# )


class UsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            self.odj.user == request.user
            or request.user.is_admin
            or request.user.is_moderator
            or request.user.is_staff
        )


class AdminOnlyPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.as_admin
            or request.user.is_staff
        )