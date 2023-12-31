from decimal import Decimal
from math import ceil
from django.shortcuts import get_object_or_404

from django.utils import timezone
from rest_framework import serializers

from reservation.models import Reservation
from utils.fields.room_fields import RoomFields
from utils.functions.verifications import checkReservationPeriod

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

    @staticmethod
    def process_conflict_reservations(
        occupied_rooms,
        all_reservations,
        dt_departure_date,
        rsv_list_conflict_free,
        rsv_list_conflict_occupied,
        rsvs_used_occupied,
    ):
        for room in occupied_rooms:
            room_entry_date = room.entry_date.replace(tzinfo=None)
            room_departure_date = room.departure_date.replace(tzinfo=None)

            for rsv in all_reservations:
                rsv_entry_date = rsv.entry_date.date()

                if dt_departure_date.date() > rsv_entry_date:
                    if rsv not in rsv_list_conflict_free:
                        rsv_list_conflict_free.append(rsv)

                if (
                    room_entry_date.date() < rsv_entry_date
                    and room_departure_date.date() <= rsv_entry_date
                    and room.quantity >= rsv.quantity
                ):
                    rsv_list_conflict_occupied.append(rsv)

            if rsv_list_conflict_occupied:
                latest_unused_rsv = next(
                    (
                        rsv
                        for rsv in sorted(
                            rsv_list_conflict_occupied,
                            key=lambda x: x.entry_date,
                        )
                        if rsv not in rsvs_used_occupied
                        and rsv in rsv_list_conflict_free
                    ),
                    None,
                )

                rsv_list_conflict_occupied.clear()

                if latest_unused_rsv:
                    rsvs_used_occupied.append(latest_unused_rsv)

    @staticmethod
    def process_reservations_with_guest(
        increase_availability,
        rsv_list_guest,
        all_reservations,
        verified_rsv_ids,
        exclude_ids,
        rsvs_used_occupied,
        rsv,
        room,
        dt_departure_date,
    ):
        if rsv in rsv_list_guest:
            increase_availability = sum(
                rsv_internal.id not in verified_rsv_ids
                and rsv_internal not in rsvs_used_occupied
                and rsv != rsv_internal
                and not checkReservationPeriod(
                    rsv.entry_date.date(),
                    dt_departure_date.date(),
                    rsv_internal.entry_date.replace(tzinfo=None),
                    rsv_internal.departure_date.replace(tzinfo=None),
                )
                for rsv_internal in all_reservations
            )

        if (
            rsv.quantity <= room.quantity
            and rsv.id not in verified_rsv_ids
            and rsv not in rsvs_used_occupied
            and rsv not in rsv_list_guest
        ):
            verified_rsv_ids.add(rsv.id)
            exclude_ids.add(room.id)

            return True, increase_availability

        return False, increase_availability

    @staticmethod
    def process_reservations_without_guest(
        rsv, room, verified_rsv_ids, exclude_ids, rsvs_used_occupied, free_unused_rooms
    ):
        if (
            rsv.quantity <= room.quantity
            and rsv.id not in verified_rsv_ids
            and rsv not in rsvs_used_occupied
        ):
            verified_rsv_ids.add(rsv.id)
            exclude_ids.add(room.id)

            return True

        return False

    def update(self, instance: Room, validated_data: dict) -> Room:
        status_data = validated_data.get("status", {})
        guest_data = validated_data.get("guest", {})
        dt_departure_date = validated_data.get("departure_date", {})
        dt_quantity = validated_data.get("quantity", {})

        image_fields = ["image2", "image3", "image4", "image5"]
        del_image_fields = [
            "delete_image2",
            "delete_image3",
            "delete_image4",
            "delete_image5",
        ]

        for image_field, del_image_field in zip(image_fields, del_image_fields):
            if validated_data.get(del_image_field):
                setattr(instance, image_field, None)

        if guest_data and dt_departure_date and dt_quantity:
            room_id_parameter = self.context["request"].parser_context["kwargs"]["pk"]
            current_room = get_object_or_404(Room, id=room_id_parameter)

            all_rooms = Room.objects.filter(hotel=current_room.hotel)
            free_rooms = all_rooms.filter(status="Free")
            occupied_rooms = all_rooms.filter(status="Occupied")

            if not free_rooms:
                raise serializers.ValidationError(
                    {"message": "There's no available rooms"}
                )

            if current_room.guest is not None and current_room.guest != guest_data:
                raise serializers.ValidationError(
                    {"message": "Cannot change the guest"}
                )

            all_reservations = Reservation.objects.filter(hotel=current_room.hotel)

            if all_reservations:
                rsv_list_guest = []

                rsv_list_conflict_free = []
                rsv_list_conflict_occupied = []
                rsvs_used_occupied = []

                increase_availability = 0

                self.process_conflict_reservations(
                    occupied_rooms=occupied_rooms,
                    all_reservations=all_reservations,
                    dt_departure_date=dt_departure_date,
                    rsv_list_conflict_free=rsv_list_conflict_free,
                    rsv_list_conflict_occupied=rsv_list_conflict_occupied,
                    rsvs_used_occupied=rsvs_used_occupied,
                )

                reservations_guest = Reservation.objects.filter(guest=guest_data)

                if reservations_guest:
                    for rsv_guest in reservations_guest:
                        rsv_dpt_date = rsv_guest.departure_date.date()
                        rsv_guest_entry_date = rsv_guest.entry_date.date()
                        current_date = timezone.now()

                        if rsv_guest_entry_date == current_date.date():
                            rsv_list_guest.append(rsv_guest)

                            if rsv_dpt_date < dt_departure_date.date():
                                rsvs_used_occupied = []

                                self.process_conflict_reservations(
                                    occupied_rooms=occupied_rooms,
                                    all_reservations=all_reservations,
                                    dt_departure_date=dt_departure_date,
                                    rsv_list_conflict_free=rsv_list_conflict_free,
                                    rsv_list_conflict_occupied=rsv_list_conflict_occupied,
                                    rsvs_used_occupied=rsvs_used_occupied,
                                )

                room_matching_condition = [
                    room for room in free_rooms if room.quantity >= dt_quantity
                ]

                free_enused_verify = False

                if current_room in room_matching_condition:
                    sorted_free_rooms = sorted(free_rooms, key=lambda x: x.quantity)
                    verified_rsv_ids = set()
                    exclude_ids = set()

                    for room in sorted_free_rooms:
                        for rsv in rsv_list_conflict_free:
                            if reservations_guest:
                                (
                                    success,
                                    increase_availability,
                                ) = self.process_reservations_with_guest(
                                    increase_availability=increase_availability,
                                    rsv_list_guest=rsv_list_guest,
                                    all_reservations=all_reservations,
                                    verified_rsv_ids=verified_rsv_ids,
                                    exclude_ids=exclude_ids,
                                    rsvs_used_occupied=rsvs_used_occupied,
                                    rsv=rsv,
                                    room=room,
                                    dt_departure_date=dt_departure_date,
                                )
                                if success:
                                    break

                            else:
                                if self.process_reservations_without_guest(
                                    rsv=rsv,
                                    room=room,
                                    verified_rsv_ids=verified_rsv_ids,
                                    exclude_ids=exclude_ids,
                                    rsvs_used_occupied=rsvs_used_occupied,
                                ):
                                    break

                    free_unused_rooms = [
                        r for r in free_rooms if r.id not in exclude_ids
                    ]

                    free_enused_verify = any(
                        r.id == current_room.id for r in free_unused_rooms
                    )

                    if not free_unused_rooms and increase_availability > 0:
                        free_enused_verify = True

                if (
                    guest_data == current_room.guest
                    and dt_departure_date == current_room.departure_date
                ):
                    free_enused_verify = True

                if not free_enused_verify:
                    raise serializers.ValidationError(
                        {"message": "There's no available rooms."}
                    )

                if len(rsv_list_guest) > 0:
                    rsv_list_guest[0].delete()

            if not instance.entry_date:
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
            instance.quantity = dt_quantity

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

        print("AAAA", validated_data)

        for key, value in validated_data.items():
            if key not in ["guest", "quantity"]:
                setattr(instance, key, value)

        instance.save()
        return instance

    class Meta:
        model = Room
        fields = RoomFields.fields
        extra_kwargs = RoomFields.extra_kwargs
