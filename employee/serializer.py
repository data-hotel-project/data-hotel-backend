from rest_framework import serializers
from .models import Employee
from address.serializer import AddressSerializer


class EmployeeSerializer(serializers.ModelSerializer):

    address = AddressSerializer


    def create(self, validated_data: dict) -> Employee:
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
        fields = ["id", "username", "email", "password", "birthdate", "nationality", "contact", "contact_aditional", "emergency_num", "job_function", "admission_date", "is_working", "address", "hotel_id"]
        extra_kwargs = {"password": {"write_only": True}}
