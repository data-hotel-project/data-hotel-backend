from rest_framework import serializers
from employee.models import Employee

from utils.fields.customUser_fields import CustomUserFields


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = CustomUserFields.fields
        extra_kwargs = CustomUserFields.extra_kwargs
