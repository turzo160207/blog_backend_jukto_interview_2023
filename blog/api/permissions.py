from rest_framework import permissions
from rest_framework.permissions import IsAdminUser, BasePermission

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
       
class IsModerator(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_moderator

    def has_object_permission(self, request, view, obj):
        user = request.user
        return user.is_moderator
    
class IsModeratorOrOwner(permissions.BasePermission):
    # def has_permission(self, request, view):
    #     return True
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        is_admin = IsAdminUser().has_permission(request, view)
        is_moderator = request.user.is_moderator
        is_owner = obj.owner == request.user
        return is_admin or is_moderator or is_owner

    
class IsAdminOrModerator(BasePermission):
    def has_permission(self, request, view):
        is_admin = IsAdminUser().has_permission(request, view)
        is_moderator = request.user.is_moderator
        return is_admin or is_moderator
    
class IsAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_admin = IsAdminUser().has_permission(request, view)
        is_owner = obj.owner == request.user
        return is_admin or is_owner

