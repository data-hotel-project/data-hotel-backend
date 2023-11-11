from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.views import Request, View


class AdminPermissions(BasePermission):
    def has_permission(self, request: Request, view: View):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and request.user.is_superuser
        )
