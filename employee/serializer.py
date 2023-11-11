from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from address.serializer import AddressSerializer
from utils.fields.employee_fields import EmployeeFields

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data: dict) -> Employee:
        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address_data = address_serializer.save()

        validated_data["address"] = address_data

        return Employee.objects.create_user(**validated_data, is_staff=True)

    def update(self, instance: Employee, validated_data: dict) -> Employee:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Employee
        fields = EmployeeFields.fields
        extra_kwargs = EmployeeFields.extra_kwargs


class EmployeeTokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        refresh = self.get_token(self.user)

        from ipdb import set_trace

        print("*" * 20)
        print(self.user)
        print("*" * 20)
        # set_trace()

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)

        return data
