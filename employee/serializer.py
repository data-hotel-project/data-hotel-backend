from rest_framework import serializers
from .models import Employee


class EmployeeSerializer(serializers.ModelSerializer):
    # address = AddressSerializer
    # hotel = HotelSerializer(read_only=True)

    class Meta:
        model = Employee
        fields = "__all__"
        # fields = ["id", "username", "email", "birthdate", "nationality",
        # "contact", "contact_aditional", "emergency_num",
        # "job_function", "admission_date", "admission_date", "is_working", "address", "hotel"]
        extra_kwargs = {"password": {"write_only": True}}
