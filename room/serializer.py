from rest_framework import serializers

from hotel.models import Hotel

# from guest.serializer import GuestSerializer

from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    hotel = serializers.PrimaryKeyRelatedField(queryset=Hotel.objects.all())
    # guest = GuestSerializer()

    # def create(self, validated_data: dict) -> Room:
    #     print("+" * 29)
    #     print(validated_data)
    #     print("+" * 29)
    #     return Room.objects.create(**validated_data)

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
