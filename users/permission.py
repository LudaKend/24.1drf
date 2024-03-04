from rest_framework.permissions import BasePermission

class ModeratorPermissionsClass(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='moderator').exists()

class UsuallyPermissionsClass(BasePermission):
    def has_permission(self, request, view):
        return request.user.groups.filter(name='usually').exists()

class OwnerPermissionsClass(BasePermission):
    def has_object_permission(self, request, view, obj):
        #print(obj.owner)          #для отладки
        if request.user == obj.owner:
            return request.method in ('GET', 'PUT', 'PATH', 'DELETE')
        else:
            return False
