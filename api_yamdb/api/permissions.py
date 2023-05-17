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


class UsersPermission(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            obj.username == request.user
            or request.user.is_admin
            or request.user.is_moderator
            
        )


class AdminOnlyPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            # request.user.is_staff
            request.user.is_authenticated
            and (request.user.is_admin
            or request.user.is_superuser)
        
        )

    # def has_object_permission(self, request, view, obj):
    #     return (
    #         request.user.is_admin
    #         # or request.user.is_staff
            
    #     )
    
# class IsAdmin(BasePermission):

#     def has_permission(self, request, view):
#         return (
#             request.user.is_authenticated
#             and (
#                 request.user.is_admin
#                 or self.is_superuser
#                 or self.is_staff
#             )
#         ) 