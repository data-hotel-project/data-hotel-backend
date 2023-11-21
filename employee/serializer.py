from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from address.models import Address

from address.serializer import AddressSerializer
from hotel.models import Hotel
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

        address, created = Address.objects.get_or_create(**address_data)

        if not created:
            hotel = Hotel.objects.filter(address=address).exists()

            if hotel:
                raise serializers.ValidationError(
                    {"address": ["hotel with this address already exists."]}
                )
            validated_data["address"] = address

            return Employee.objects.create_user(**validated_data, is_staff=True)

        validated_data["address"] = address

        return Employee.objects.create_user(**validated_data, is_staff=True)

    def update(self, instance: Employee, validated_data: dict) -> Employee:
        address_instance = instance.address
        address_data = validated_data.get("address", {})

        is_address_changed = any(
            getattr(address_instance, field) != value
            for field, value in address_data.items()
        )

        if is_address_changed:
            combined_data = {**address_instance.__dict__, **address_data}

            combined_data.pop("_state", None)
            combined_data.pop("id", None)

            existing_address = Address.objects.filter(**combined_data).first()

            if existing_address:
                hotel = Hotel.objects.filter(address=existing_address).exists()

                if hotel:
                    raise serializers.ValidationError(
                        {"address": ["hotel with this address already exists."]}
                    )

                instance.address = existing_address
            else:
                new_address_instance = Address.objects.create(
                    street=address_data.get("street", address_instance.street),
                    number=address_data.get("number", address_instance.number),
                    city=address_data.get("city", address_instance.city),
                    state=address_data.get("state", address_instance.state),
                    complement=address_data.get(
                        "complement", address_instance.complement
                    ),
                )

                instance.address = new_address_instance
                instance.save()

        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            elif key == "address":
                pass
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Employee
        fields = EmployeeFields.fields
        extra_kwargs = EmployeeFields.extra_kwargs
