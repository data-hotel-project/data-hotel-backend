from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from employee.permissions import IsEmployee

from utils.permissions import IsAdmin

from .models import Reservation
from .permissions import IsGuest, IsGuestOwner
from .serializer import ReservationSerializer

from rest_framework.response import Response
from datetime import datetime
from hotel.models import Hotel


class ReservationListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuest]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def create(self, request, *args, **kwargs):
        hotel_id_parameter = self.request.data["hotel"]
        hotel_reservations = Reservation.objects.filter(hotel=hotel_id_parameter)
        hotel = Hotel.objects.filter(id=hotel_id_parameter).first()

        rsv_list = []
        dt_entry_date = datetime.fromisoformat(self.request.data["entry_date"])

        for rsv in hotel_reservations:
            rsv_departure_date = rsv.departure_date.replace(tzinfo=None)

            if rsv_departure_date >= dt_entry_date:
                rsv_list.append(rsv)

        if hotel.num_rooms <= len(rsv_list):
            return Response({"message": "Hotel is full"}, status=400)

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
