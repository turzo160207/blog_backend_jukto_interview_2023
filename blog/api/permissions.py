from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, BasePermission

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
    
# class IsModerator(permissions.BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method not in permissions.SAFE_METHODS:
#             return False
#         return False
    
class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_moderator

    def has_object_permission(self, request, view, obj):
        user = request.user
        print('User is moderator:', user.is_moderator)
        print('Object owner is moderator:', obj.is_moderator)
        return user.is_moderator
    
class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        is_admin = IsAdminUser().has_permission(request, view)
        is_moderator = request.user.is_moderator
        return is_admin or is_moderator