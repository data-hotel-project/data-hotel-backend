from rest_framework import serializers
from .models import Hotel
from address.serializer import AddressSerializer


class HotelSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Hotel
        fields = ["id", "name", "email", "password", "num_rooms", "address"]
