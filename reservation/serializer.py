from rest_framework import serializers

from room.models import Room
from utils.fields.reservation_fields import ReservationFields
from utils.functions.verifications import checkReservationPeriod, loopingRooms
from .models import Reservation


class ReservationSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        dt_entry_date = validated_data.get("entry_date", {})
        dt_departure_date = validated_data.get("departure_date", {})

        all_reservations = Reservation.objects.filter(hotel=instance.hotel)
        occupied_rooms = Room.objects.filter(hotel=instance.hotel, status="Occupied")
        rooms_free = Room.objects.filter(hotel=instance.hotel, status="Free")
        rsv_count_match = 0
        room_count = 0

        if dt_entry_date or dt_departure_date:
            dt_entry_date = dt_entry_date.date()
            dt_departure_date = dt_departure_date.date()

            if all_reservations:
                for room in occupied_rooms:
                    if dt_entry_date:
                        room_departure_date = room.departure_date.replace(tzinfo=None)

                        if dt_entry_date >= room_departure_date.date():
                            room_count += 1
                    else:
                        room_departure_date = room.departure_date.replace(tzinfo=None)

                        if instance.entry_date >= room_departure_date.date():
                            room_count += 1

                for rsv in all_reservations:
                    rsv_departure_date = rsv.departure_date.replace(tzinfo=None)
                    rsv_entry_date = rsv.entry_date.replace(tzinfo=None)

                    if dt_entry_date and not dt_departure_date:
                        check = checkReservationPeriod(
                            dt_entry_date,
                            dt_departure_date,
                            rsv_entry_date,
                            rsv_departure_date,
                        )
                        if check:
                            rsv_count_match += 1

                    elif dt_departure_date and not dt_entry_date:
                        if (
                            instance.entry_date.date() >= rsv_entry_date.date()
                            and instance.entry_date.date() < rsv_departure_date.date()
                            or (
                                instance.entry_date.date() <= rsv_entry_date.date()
                                and dt_departure_date > rsv_entry_date.date()
                            )
                        ):
                            rsv_count_match += 1

                    elif dt_departure_date and dt_entry_date:
                        check = checkReservationPeriod(
                            dt_entry_date,
                            dt_departure_date,
                            rsv_entry_date,
                            rsv_departure_date,
                        )

                        if check:
                            rsv_count_match += 1
                from ipdb import set_trace

                set_trace()
                if len(rooms_free) + room_count - rsv_count_match <= 0:
                    raise serializers.ValidationError(
                        {"message": "There's no available rooms."}
                    )

            else:
                room_count = loopingRooms(occupied_rooms, dt_entry_date=dt_entry_date)

                if room_count == 0 and len(rooms_free) == 0:
                    raise serializers.ValidationError(
                        {"message": "There's no available rooms."}
                    )

        for key, value in validated_data.items():
            if key != "guest" and key != "hotel":
                setattr(instance, key, value)

        instance.save()
        return instance

    class Meta:
        model = Reservation
        fields = ReservationFields.fields
        read_only_fields = ReservationFields.read_only_fields
