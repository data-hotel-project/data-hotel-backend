from rest_framework import generics
from .serializer import ReservationSerializer
from .models import Reservation
from .permissions import IsGuest
from utils.permissions import IsAdmin
from rest_framework_simplejwt.authentication import JWTAuthentication

class ReservationListCreateView(generics.ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class ReservationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuest | IsAdmin]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_url_kwarg = "pk"
