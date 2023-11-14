from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View


class IsAddressOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj):
        return request.user.id == obj.id