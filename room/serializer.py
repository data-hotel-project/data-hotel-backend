from decimal import Decimal
from math import ceil
from django.utils import timezone
from rest_framework import serializers
from hotel.models import Hotel
from reservation.models import Reservation

from utils.fields.room_fields import RoomFields

from .models import Room
from rest_framework.response import Response

class RoomSerializer(serializers.ModelSerializer):
    full_url = serializers.SerializerMethodField()
    full_url2 = serializers.SerializerMethodField()
    full_url3 = serializers.SerializerMethodField()
    full_url4 = serializers.SerializerMethodField()
    full_url5 = serializers.SerializerMethodField()

    def get_full_url(self, obj):
        if obj.image:
            return obj.image.url

    def get_full_url2(self, obj):
        if obj.image2:
            return obj.image2.url

    def get_full_url3(self, obj):
        if obj.image3:
            return obj.image3.url

    def get_full_url4(self, obj):
        if obj.image4:
            return obj.image4.url

    def get_full_url5(self, obj):
        if obj.image5:
            return obj.image5.url

    def update(self, instance: Room, validated_data: dict) -> Room:
        room_id_parameter = self.context['request'].parser_context['kwargs']['pk']
        room = Room.objects.filter(id=room_id_parameter).first()
        rooms_hotel = Room.objects.filter(hotel=room.hotel, status='Free')

        if len(rooms_hotel) == 0:
            raise serializers.ValidationError({"message": "There's no available rooms"})
        
        hotel_reservations = Reservation.objects.filter(hotel=room.hotel)

        for rsv in hotel_reservations:
            # from ipdb import set_trace
            # set_trace()
            # ...
            rsv_entry_date = rsv.entry_date.date()

        guest_data = validated_data.get("guest", {})
        departure_date_data = validated_data.get("departure_date", {})

        if guest_data and departure_date_data:
            instance.entry_date = timezone.now()

            time_difference = departure_date_data - instance.entry_date

            difference_in_seconds = Decimal(time_difference.total_seconds())

            days_total = difference_in_seconds / 60 / 60 / 24

            if days_total > time_difference.days:
                instance.total_value = ceil(days_total) * instance.daily_rate

        else:
            raise serializers.ValidationError(
                {"errors": ["Guest can only be passed along with the departure_date."]}
            )

        for key, value in validated_data.items():
            if key != "guest":
                setattr(instance, key, value)

        instance.save()
        return instance

    class Meta:
        model = Room
        fields = RoomFields.fields
        extra_kwargs = RoomFields.extra_kwargs
