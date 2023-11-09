from rest_framework import serializers

from address.serializer import AddressSerializer

from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data: dict) -> Employee:
        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address_data = address_serializer.save()

        validated_data["address"] = address_data

        return Employee.objects.create_user(**validated_data)

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
        # fields = "__all__"
        fields = [
            "id",
            "username",
            "email",
            "password",
            "birthdate",
            "nationality",
            "contact",
            "contact_aditional",
            "emergency_num",
            "job_function",
            "admission_date",
            "is_working",
            "address",
            "hotel",
        ]
        extra_kwargs = {"password": {"write_only": True}}
