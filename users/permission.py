from rest_framework.permissions import BasePermission

class ModeratorPermissionsClass(BasePermission):
    def has_permission(self, request, view):
        print(request.user.groups.filter(name='moderator').exists())
        return request.user.groups.filter(name='moderator').exists()

class UsuallyPermissionsClass(BasePermission):
    def has_permission(self, request, view):
        print(f"usually: {request.user.groups.filter(name='usually').exists()}")
        return request.user.groups.filter(name='usually').exists()
