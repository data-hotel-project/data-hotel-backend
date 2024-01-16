from rest_framework import serializers
from employee.models import Employee
from address.serializer import AddressSerializer

from utils.fields.customUser_fields import CustomUserFields


class CustomUserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Employee
        fields = CustomUserFields.fields
        extra_kwargs = CustomUserFields.extra_kwargs
