from datetime import datetime

import pytz
from django.utils import timezone
from ipdb import set_trace
from rest_framework.response import Response

from room.models import Room
from utils.functions.verifications import loopingRooms


class ReservationMixin:
    def create(self, request, *args, **kwargs):
        data = self.request.data
        hotel_id_parameter = self.request.data["hotel"]
        occupied_rooms = Room.objects.filter(
            hotel=hotel_id_parameter, status="Occupied"
        )
        free_rooms = Room.objects.filter(hotel=hotel_id_parameter, status="Free")

        saopaulo_tz = pytz.timezone("America/Sao_Paulo")

        dt_departure_date = saopaulo_tz.localize(
            datetime.fromisoformat(data["departure_date"])
        ).date()

        dt_entry_date = saopaulo_tz.localize(
            datetime.fromisoformat(data["entry_date"])
        ).date()

        currentDate = timezone.now().date()

        if dt_entry_date < currentDate:
            return Response(
                {"message": "Entry date smaller than current date"}, status=400
            )

        if dt_departure_date < dt_entry_date:
            return Response(
                {"message": "Departure date smaller than entry date"}, status=400
            )

        room_count, rsv_count_match, free_unused_rooms_qt = loopingRooms(
            occupied_rooms,
            data,
            hotel_id_parameter=hotel_id_parameter,
            free_rooms=free_rooms,
        )

        if room_count + free_unused_rooms_qt - rsv_count_match <= 0:
            return Response({"message": "Hotel is full"}, status=400)

        return super().create(request, *args, **kwargs)
