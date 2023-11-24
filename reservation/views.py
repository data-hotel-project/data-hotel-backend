from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from employee.permissions import IsEmployee
from room.models import Room

from utils.permissions import IsAdmin

from .models import Reservation
from .permissions import IsGuest, IsGuestOwner
from .serializer import ReservationSerializer

from rest_framework.response import Response
from datetime import datetime

# from hotel.models import Hotel


class ReservationListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuest]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        from ipdb import set_trace

        hotel_id_parameter = self.request.data["hotel"]
        all_reservations = Reservation.objects.filter(hotel=hotel_id_parameter)
        # hotel = Hotel.objects.filter(id=hotel_id_parameter).first()
        occupied_rooms = Room.objects.filter(
            hotel=hotel_id_parameter, status="Occupied"
        )
        rooms_free = Room.objects.filter(hotel=hotel_id_parameter, status="Free")
        rooms_all = Room.objects.filter(hotel=hotel_id_parameter)

        rsv_list_match = []
        room_list = []
        dt_entry_date = datetime.fromisoformat(self.request.data["entry_date"]).date()
        dt_departure_date = datetime.fromisoformat(
            self.request.data["departure_date"]
        ).date()

        # Percorre todas as reservas
        if all_reservations:
            for room in occupied_rooms:
                room_departure_date = room.departure_date.replace(tzinfo=None)

                if dt_entry_date >= room_departure_date.date():
                    # 3
                    room_list.append(room)

            for rsv in all_reservations:
                rsv_departure_date = rsv.departure_date.replace(tzinfo=None)
                rsv_entry_date = rsv.entry_date.replace(tzinfo=None)

                # if rsv_departure_date >= dt_entry_date:
                #     rsv_list_match.append(rsv)
                if (
                    dt_entry_date >= rsv_entry_date.date()
                    and dt_entry_date < rsv_departure_date.date()
                    or (
                        dt_entry_date <= rsv_entry_date.date()
                        and dt_departure_date > rsv_entry_date.date()
                    )
                ):
                    # 2
                    rsv_list_match.append(rsv)
            # if hotel.num_rooms <= len(rsv_list_match) and len(room_list) >= len(rsv_list_match):
            #     return Response({"message": "Hotel is full"}, status=400)

            set_trace()
            if (
                len(room_list) == 0
                or len(rooms_free) + len(room_list) - len(rsv_list_match) == 0
            ):
                return Response({"message": "Hotel is full"}, status=400)

            return super().create(request, *args, **kwargs)

        elif rooms_free:
            return super().create(request, *args, **kwargs)

    def get_queryset(self):
        hotel_id_parameter = self.request.query_params.get("hotel_id")
        if hotel_id_parameter:
            return Reservation.objects.filter(hotel=hotel_id_parameter)

        return super().get_queryset()

    def perform_create(self, serializer):
        return serializer.save(guest=self.request.user.guest)


class ReservationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuestOwner | IsEmployee | IsAdmin]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_url_kwarg = "pk"

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     if getattr(instance, '_prefetched_objects_cache', None):
    #         # If 'prefetch_related' has been applied to a queryset, we need to
    #         # forcibly invalidate the prefetch cache on the instance.
    #         instance._prefetched_objects_cache = {}

    #     return Response(serializer.data)
