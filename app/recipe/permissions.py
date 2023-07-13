from rest_framework.permissions import BasePermission


class IsRecipePublicOrAuthenticated(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user.is_authenticated
