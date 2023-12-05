from decimal import Decimal
from math import ceil

from django.utils import timezone
from rest_framework import serializers

from reservation.models import Reservation
from utils.fields.room_fields import RoomFields

from .models import Room


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
        status_data = validated_data.get("status", {})

        guest_data = validated_data.get("guest", {})
        dt_departure_date = validated_data.get("departure_date", {})
        dt_quantity = validated_data.get("quantity", {})

        from ipdb import set_trace

        if guest_data and dt_departure_date and dt_quantity:
            room_id_parameter = self.context["request"].parser_context["kwargs"]["pk"]
            room = Room.objects.filter(id=room_id_parameter).first()
            rooms_free = Room.objects.filter(hotel=room.hotel, status="Free")
            occupied_rooms = Room.objects.filter(hotel=room.hotel, status="Occupied")

            if len(rooms_free) == 0 and not guest_data:
                raise serializers.ValidationError(
                    {"message": "There's no available rooms"}
                )

            if room.guest and room.guest != guest_data:
                raise serializers.ValidationError(
                    {"message": "Cannot change the guest"}
                )

            all_reservations = Reservation.objects.filter(hotel=room.hotel)

            if all_reservations:
                rsv_count_match_primary = 0
                rsv_list_guest = []
                rsv_count_match = 0
                room_list = 0

                for rsv in all_reservations:
                    rsv_entry_date = rsv.entry_date.date()

                    if dt_departure_date.date() > rsv_entry_date:
                        rsv_count_match_primary += 1

                reservations_guest = Reservation.objects.filter(guest=guest_data)

                if reservations_guest:
                    for rsv_guest in reservations_guest:
                        rsv_dpt_date = rsv_guest.departure_date.date()
                        rsv_guest_entry_date = rsv_guest.entry_date.date()
                        current_date = timezone.now()

                        if rsv_guest_entry_date == current_date.date():
                            rsv_list_guest.append(rsv_guest)

                            if dt_departure_date:
                                if rsv_dpt_date < dt_departure_date.date():
                                    for rsv in all_reservations:
                                        rsv_entry_date = rsv.entry_date.date()

                                        if dt_departure_date.date() > rsv_entry_date:
                                            if rsv_guest != rsv:
                                                rsv_count_match += 1

                                    for room in occupied_rooms:
                                        room_departure_date = (
                                            room.departure_date.replace(tzinfo=None)
                                        )

                                        if (
                                            rsv_guest_entry_date
                                            <= room_departure_date.date()
                                        ):
                                            room_list += 1

                                    if (
                                        len(rooms_free) + room_list - rsv_count_match
                                        <= 0
                                    ):
                                        raise serializers.ValidationError(
                                            {"message": "There's no available rooms."}
                                        )

                if (
                    len(rooms_free) <= rsv_count_match_primary
                    and len(rsv_list_guest) == 0
                ):
                    raise serializers.ValidationError(
                        {"message": "There's no available rooms."}
                    )

                if len(rsv_list_guest) > 0:
                    rsv_list_guest[0].delete()

            if instance.entry_date is None:
                instance.entry_date = timezone.now()

            time_difference = dt_departure_date - instance.entry_date

            if time_difference.days < 0:
                raise serializers.ValidationError(
                    {"errors": ["Departure date smaller than entry date"]}
                )

            difference_in_seconds = Decimal(time_difference.total_seconds())

            days_total = difference_in_seconds / 60 / 60 / 24

            if days_total > time_difference.days:
                instance.total_value = ceil(days_total) * instance.daily_rate

            instance.guest = guest_data
            instance.status = "Occupied"

        elif guest_data and dt_departure_date and not dt_quantity:
            raise serializers.ValidationError(
                {"errors": ["'Quantity' field is mandatory at check in"]}
            )

        elif guest_data and not dt_departure_date:
            raise serializers.ValidationError(
                {"errors": ["Guest can only be passed along with the departure_date."]}
            )

        elif status_data == "Free":
            instance.entry_date = None
            instance.departure_date = None
            instance.guest = None
            instance.total_value = "0.00"

        for key, value in validated_data.items():
            if key != "guest" and key != "quantity":
                setattr(instance, key, value)

        instance.save()
        return instance

    class Meta:
        model = Room
        fields = RoomFields.fields
        extra_kwargs = RoomFields.extra_kwargs
