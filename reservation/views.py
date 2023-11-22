from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from employee.permissions import IsEmployee

from utils.permissions import IsAdmin

from .models import Reservation
from .permissions import IsGuest, IsGuestOwner
from .serializer import ReservationSerializer


class ReservationListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuest]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

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
