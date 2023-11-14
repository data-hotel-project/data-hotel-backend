from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View
from .models import Guest


class IsGuestAndOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Guest):
        return request.user.id == obj.id