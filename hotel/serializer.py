from rest_framework import serializers

from utils.fields.hotel_fields import HotelFields
from .models import Hotel
from address.serializer import AddressSerializer


class HotelSerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    full_url = serializers.SerializerMethodField()

    def get_full_url(self, obj):
        return obj.image.url

    def create(self, validated_data: dict) -> Hotel:
        address_data = validated_data.pop("address")

        address_serializer = AddressSerializer(data=address_data)
        address_serializer.is_valid(raise_exception=True)

        address_data = address_serializer.save()

        validated_data["address"] = address_data

        return Hotel.objects.create(**validated_data)

    class Meta:
        model = Hotel
        fields = HotelFields.fields
