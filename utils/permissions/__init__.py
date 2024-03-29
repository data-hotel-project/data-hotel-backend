from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import Request, View


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_superuser


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
        )


class IsAuthenticated(BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.user.is_authenticated
