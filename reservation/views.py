from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.permissions import IsAdmin

from .models import Reservation
from .permissions import IsGuest
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

    def post(self, request, *args, **kwargs):
        # from ipdb import set_trace

        # set_trace()
        return super().post(request, *args, **kwargs)

    def perform_create(self, serializer):
        print("eu cheiguei aqui")

        return serializer.save(guest=self.request.user)


class ReservationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuest | IsAdmin]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_url_kwarg = "pk"
