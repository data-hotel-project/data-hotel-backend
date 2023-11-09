from rest_framework import serializers
from .models import Hotel
from address.serializer import AddressSerializer


class HotelSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    def create(self, validated_data: dict) -> Hotel:
        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address_data = address_serializer.save()

        validated_data["address"] = address_data

        return Hotel.objects.create(**validated_data)

    class Meta:
        model = Hotel
        fields = ["id", "name", "email", "password", "num_rooms", "address"]
