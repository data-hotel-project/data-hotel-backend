from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from rest_framework import serializers

from employee.models import Employee
from guest.models import Guest


class EmailOrUsernameModelBackend(ModelBackend):
    def get_user_model(self, request):
        url_route = request.path_info.split("/")[2]

        return (
            Guest
            if "guest" in url_route
            else Employee
            if "employee" in url_route
            else get_user_model()
        )

    def authenticate(self, request, username=None, email=None, password=None, **kwargs):
        userModel = self.get_user_model(request)

        if email:
            try:
                print("Entrou email")
                user = userModel.objects.get(email=email)
            except userModel.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Invalid credentials"]}
                )

        else:
            try:
                print("Entrou Username")
                user = userModel.objects.get(username=username)
            except userModel.DoesNotExist:
                raise serializers.ValidationError(
                    {"non_field_errors": ["Invalid credentials"]}
                )

        if user.check_password(password):
            return user

        return None
