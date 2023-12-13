from copy import deepcopy
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
            current_room = Room.objects.filter(id=room_id_parameter).first()
            free_rooms = Room.objects.filter(hotel=current_room.hotel, status="Free")
            occupied_rooms = Room.objects.filter(
                hotel=current_room.hotel, status="Occupied"
            )

            if len(free_rooms) == 0:
                raise serializers.ValidationError(
                    {"message": "There's no available rooms"}
                )

            if current_room.guest and current_room.guest != guest_data:
                raise serializers.ValidationError(
                    {"message": "Cannot change the guest"}
                )

            all_reservations = Reservation.objects.filter(hotel=current_room.hotel)

            if all_reservations:
                rsv_count_match_primary = 0
                rsv_list_guest = []
                rsv_count_match = 0
                room_list = 0

                rsv_list_verify = []
                rsvs_used_verify = []

                decrease_rsv_count_match_primary = 0

                rsv_list_free = []

                for room in occupied_rooms:
                    room_entry_date = room.entry_date.replace(tzinfo=None)
                    room_departure_date = room.departure_date.replace(tzinfo=None)

                    for rsv in all_reservations:
                        rsv_entry_date = rsv.entry_date.date()

                        if dt_departure_date.date() > rsv_entry_date:
                            rsv_count_match_primary += 1

                            if rsv not in rsv_list_free:
                                rsv_list_free.append(rsv)

                        if (
                            room_entry_date.date() < rsv_entry_date
                            and room_departure_date.date() <= rsv_entry_date
                            and room.quantity >= rsv.quantity
                        ):
                            rsv_list_verify.append(rsv)

                    if rsv_list_verify:
                        latest_unused_rsv = next(
                            (
                                rsv
                                for rsv in sorted(
                                    rsv_list_verify, key=lambda x: x.entry_date
                                )
                                if rsv not in rsvs_used_verify and rsv in rsv_list_free
                            ),
                            None,
                        )

                        rsv_list_verify.clear()

                        if latest_unused_rsv:
                            rsvs_used_verify.append(latest_unused_rsv)
                            decrease_rsv_count_match_primary += 1

                if len(occupied_rooms) != 0:
                    rsv_count_match_primary = int(
                        rsv_count_match_primary / len(occupied_rooms)
                    )

                rsv_count_match_primary -= decrease_rsv_count_match_primary

                reservations_guest = Reservation.objects.filter(guest=guest_data)

                if reservations_guest:
                    for rsv_guest in reservations_guest:
                        rsv_dpt_date = rsv_guest.departure_date.date()
                        rsv_guest_entry_date = rsv_guest.entry_date.date()
                        current_date = timezone.now()

                        if rsv_guest_entry_date == current_date.date():
                            rsv_list_guest.append(rsv_guest)

                            if rsv_dpt_date < dt_departure_date.date():
                                for rsv in all_reservations:
                                    rsv_entry_date = rsv.entry_date.date()

                                    if dt_departure_date.date() > rsv_entry_date:
                                        if rsv_guest != rsv:
                                            rsv_count_match += 1

                                for room in occupied_rooms:
                                    room_departure_date = room.departure_date.replace(
                                        tzinfo=None
                                    )

                                    if (
                                        rsv_guest_entry_date
                                        <= room_departure_date.date()
                                    ):
                                        room_list += 1

                                if len(free_rooms) + room_list - rsv_count_match <= 0:
                                    raise serializers.ValidationError(
                                        {"message": "There's no available rooms."}
                                    )

                room_matching_condition = [
                    room for room in free_rooms if room.quantity >= dt_quantity
                ]

                free_enused_verify = False

                if current_room in room_matching_condition:
                    sorted_free_rooms = sorted(free_rooms, key=lambda x: x.quantity)
                    verified_rsv_ids = set()

                    free_unused_rooms = deepcopy(free_rooms)

                    for room in sorted_free_rooms:
                        for rsv in rsv_list_free:
                            if (
                                rsv.quantity <= room.quantity
                                and rsv.id not in verified_rsv_ids
                                and rsv not in rsvs_used_verify
                            ):
                                verified_rsv_ids.add(rsv.id)
                                free_unused_rooms = free_unused_rooms.exclude(
                                    id=room.id
                                )
                                break

                    free_enused_verify = any(
                        r.id == current_room.id for r in free_unused_rooms
                    )

                # print("AAAA", room_matching_condition)
                # print("BBBB", rsv_count_match_primary)
                # print("CCCC", len(rsv_list_guest))
                # print("DDDD", free_enused_verify)

                if not free_enused_verify and len(rsv_list_guest) == 0:
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
