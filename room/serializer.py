from rest_framework import serializers
from .models import Room
from hotel.serializer import HotelSerializer
from guest.serializer import GuestSerializer


class RoomSerializer(serializers.ModelSerializer):
    hotel = HotelSerializer()
    guest = GuestSerializer(many=True)
    
    class Meta:
        model = Room
        fields = '__all__'
        depth = 1