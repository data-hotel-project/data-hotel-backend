from rest_framework.permissions import BasePermission
from rest_framework.views import Request, View

from reservation.models import Reservation


class IsGuest(BasePermission):
    def has_permission(self, request: Request, view: View):
        return not request.user.is_staff


class IsGuestOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: Reservation):
        return request.user.is_staff or obj.guest == request.user.guest
