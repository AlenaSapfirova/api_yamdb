from rest_framework import permissions


class UsersPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
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
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.user.as_admin
            or request.user.is_staff
        )
