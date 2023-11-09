from rest_framework import serializers

from address.serializer import AddressSerializer

from .models import Guest


class GuestSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data: dict) -> Guest:
        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address_data = address_serializer.save()

        validated_data["address"] = address_data

        return Guest.objects.create(**validated_data)

    def update(self, instance: Guest, validated_data: dict) -> Guest:
        for key, value in validated_data.items():
            if key == "password":
                instance.set_password(value)
            else:
                setattr(instance, key, value)

        instance.save()

        return instance

    class Meta:
        model = Guest
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
        }
        
