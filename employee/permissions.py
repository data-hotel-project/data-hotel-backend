from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View

from .models import Employee


class IsEmployeeAndOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Employee):
        return request.method != "DELETE" and request.user.id == obj.id
