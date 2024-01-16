import re
from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import serializers, status
from rest_framework.response import Response

from employee.models import Employee
from guest.models import Guest
from rest_framework_simplejwt.tokens import RefreshToken


class EmailOrUsernameModelBackend(ModelBackend):
    def get_user_model(self, request):
        url_route = request.path_info.split("/")[1]

        return (
            Guest
            if "guest" in url_route
            else Employee
            if "employee" in url_route
            else get_user_model()
        )

    def authenticate(self, request, username=None, password=None, **kwargs):
        userModel = self.get_user_model(request)

        r = re.compile(r".+@(?:.+\.)+[a-zA-Z]{2,}$")

        if r.match(username):
            try:
                user = userModel.objects.get(email=username)
            except userModel.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Invalid credentials"]}
                )

        else:
            try:
                user = userModel.objects.get(username=username)
            except userModel.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Invalid credentials"]}
                )
        if user.check_password(password):
            return user

        return None

    def handle_login_auth(self, request):
        email_or_username = request.data.get("username")
        password = request.data.get("password")

        if not email_or_username or not password:
            return Response(
                {"error": "username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=email_or_username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)

            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "is_staff": user.is_staff,
                    "is_superuser": user.is_superuser,
                    "hotel": user.hotel_id if isinstance(user, Employee) else None,
                },
            }

            return Response(data, status=status.HTTP_200_OK)
