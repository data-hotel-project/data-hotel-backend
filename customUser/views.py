from django.core.exceptions import ObjectDoesNotExist
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from guest.models import Guest
from utils.permissions import IsAuthenticated

from employee.models import Employee
from .serializer import CustomUserSerializer


class GetLoggedUser(RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        user_id = self.request.auth.payload["user_id"]
        try:
            user = Employee.objects.get(id=user_id)
            return user
        except ObjectDoesNotExist:
            user = Guest.objects.get(id=user_id)
            return user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)

        return Response(serializer.data)
