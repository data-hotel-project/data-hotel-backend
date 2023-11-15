from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View


class IsGuest(BasePermission):
    def has_permission(self, request: Request, view: View):
        return not request.user.is_staff
