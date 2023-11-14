import re
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from address.serializer import AddressSerializer
from utils.fields.employee_fields import EmployeeFields

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Employee.objects.all())],
    )

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
        email_or_username = attrs.get("email")
        password = attrs.get("password")

        if email_or_username and password:
            user = self.get_user(email_or_username)
            if user and user.check_password(password):
                refresh = self.get_token(user)

                data = {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }

                return data

        raise serializers.ValidationError("Invalid credentials")

    def get_user(self, email_or_username):
        r = re.compile(r".+@(?:.+\.)+[a-zA-Z]{2,}$")

        if r.match(email_or_username):
            try:
                user = Employee.objects.get(email=email_or_username)
                return user
            except Employee.DoesNotExist:
                return None

        else:
            try:
                user = Employee.objects.get(username=email_or_username)
                return user
            except Employee.DoesNotExist:
                return None
