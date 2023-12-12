from datetime import datetime
from reservation.models import Reservation
from room.models import Room
from rest_framework.response import Response

from utils.functions.verifications import loopingRooms

from ipdb import set_trace


class ReservationMixin:
    def create(self, request, *args, **kwargs):
        data = self.request.data
        hotel_id_parameter = self.request.data["hotel"]
        all_reservations = Reservation.objects.filter(hotel=hotel_id_parameter)
        occupied_rooms = Room.objects.filter(
            hotel=hotel_id_parameter, status="Occupied"
        )
        free_rooms = Room.objects.filter(hotel=hotel_id_parameter, status="Free")

        room_quantity_matching_condition = 0
        room_count = 0

        dt_quantity = self.request.data["quantity"]
        dt_entry_date = datetime.fromisoformat(self.request.data["entry_date"]).date()

        if free_rooms:
            room_quantity_matching_condition = sum(
                room.quantity >= dt_quantity for room in free_rooms
            )

        if all_reservations:
            room_count, rsv_count_match, free_unused_rooms_count = loopingRooms(
                occupied_rooms,
                data,
                hotel_id_parameter=hotel_id_parameter,
                free_rooms=free_rooms,
            )

            set_trace()

            return Response({"message": "Hotellllll is full"}, status=400)
            if free_unused_rooms_count + room_count - rsv_count_match <= 0:
                return Response({"message": "Hotel is full"}, status=400)

            return super().create(request, *args, **kwargs)

        else:
            room_count = loopingRooms(occupied_rooms, data, free_rooms=free_rooms)
            return Response({"message": "Hotellllll is full"}, status=400)

            if room_count == 0:
                return Response({"message": "Hotel is full"}, status=400)

            return super().create(request, *args, **kwargs)
