from datetime import datetime
from reservation.models import Reservation
from room.models import Room
from rest_framework.response import Response

from utils.functions.verifications import checkReservationPeriod, loopingRooms


class ReservationMixin:
    def create(self, request, *args, **kwargs):
        hotel_id_parameter = self.request.data["hotel"]
        all_reservations = Reservation.objects.filter(hotel=hotel_id_parameter)
        occupied_rooms = Room.objects.filter(
            hotel=hotel_id_parameter, status="Occupied"
        )
        rooms_free = Room.objects.filter(hotel=hotel_id_parameter, status="Free")

        room_quantity_matching_condition = 0
        rsv_count_match = 0
        room_count = 0

        dt_quantity = self.request.data["quantity"]
        dt_entry_date = datetime.fromisoformat(self.request.data["entry_date"]).date()
        dt_departure_date = datetime.fromisoformat(
            self.request.data["departure_date"]
        ).date()

        from ipdb import set_trace

        if rooms_free:
            room_quantity_matching_condition = sum(
                room.quantity >= dt_quantity for room in rooms_free
            )

        if all_reservations:
            room_count = loopingRooms(
                occupied_rooms, dt_entry_date, dt_quantity, hotel_id_parameter
            )

            for rsv in all_reservations:
                rsv_departure_date = rsv.departure_date.replace(tzinfo=None)
                rsv_entry_date = rsv.entry_date.replace(tzinfo=None)

                check = checkReservationPeriod(
                    dt_entry_date,
                    dt_departure_date,
                    rsv_entry_date,
                    rsv_departure_date,
                )
                if check:
                    rsv_count_match += 1

            if room_quantity_matching_condition + room_count - rsv_count_match <= 0:
                return Response({"message": "Hotel is full"}, status=400)

            return super().create(request, *args, **kwargs)

        elif room_quantity_matching_condition > 0:
            return super().create(request, *args, **kwargs)
        else:
            room_count = loopingRooms(occupied_rooms, dt_entry_date, dt_quantity)

            if room_count == 0:
                return Response({"message": "Hotel is full"}, status=400)

            return super().create(request, *args, **kwargs)
