from rest_framework import serializers
from .models import Reservation
from guest.serializer import GuestSerializer

class ReservationSerializer(serializers.ModelSerializer):
    guest = GuestSerializer()

    class Meta:
        model = Reservation
        fields = '__all__'
        depth = 1