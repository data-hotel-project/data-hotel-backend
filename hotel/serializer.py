from rest_framework import serializers
from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    # address = AddressSerializer

    class Meta:
        model = Hotel
        fields = "__all__"
