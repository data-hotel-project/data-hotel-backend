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

        room_count, rsv_count_match, free_unused_rooms_qt = loopingRooms(
            occupied_rooms,
            data,
            hotel_id_parameter=hotel_id_parameter,
            free_rooms=free_rooms,
        )

        if room_count + free_unused_rooms_qt - rsv_count_match <= 0:
            return Response({"message": "Hotel is full"}, status=400)

        return super().create(request, *args, **kwargs)
