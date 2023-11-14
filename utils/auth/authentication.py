from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import serializers

from employee.models import Employee
from guest.models import Guest


class EmailOrUsernameModelBackend(ModelBackend):
    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        url_route = request._request.path_info.split("/")[2]
        user_model = (
            Guest
            if "guest" in url_route
            else Employee
            if "employee" in url_route
            else None
        )

        if user_model is None:
            user_model = get_user_model()

        if email:
            try:
                print("Entrou email")
                user = user_model.objects.get(email=email)
            except user_model.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Invalid credentials"]}
                )

        else:
            try:
                print("Entrou Username")
                user = user_model.objects.get(username=username)
            except user_model.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Invalid credentials"]}
                )

        if user.check_password(password):
            return user

        return None
