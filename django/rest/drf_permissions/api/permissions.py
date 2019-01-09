from rest_framework.permissions import BasePermission


class IsSuperUserOrOwnerDelete(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.permissions & 4:
            return True
        elif request.user == obj.user:
            return True
        else:
            return False

class IsOwnerUpdate(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user



