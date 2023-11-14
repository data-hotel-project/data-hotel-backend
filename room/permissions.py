from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View


class IsStaff(BasePermission):
    def has_permission(self, request: Request, view: View):
        return request.method is not 'DELETE' or request.user.is_staff