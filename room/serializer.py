from rest_framework import serializers

from hotel.models import Hotel

# from guest.serializer import GuestSerializer

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())

    class Meta:
        model = Room
        # fields = "__all__"
        fields = [
            "id",
            "number",
            "quantity",
            "status",
            "entry_date",
            "departure_date",
            "total_value",
            "guest",
            "hotel",
        ]
        depth = 1
