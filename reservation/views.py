from rest_framework import generics
from .serializer import ReservationSerializer
from .models import Reservation
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated


class ReservationListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    # mudar para "ser GUEST"
    # permission_classes = [IsAuthenticated]

    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def post(self, request, *args, **kwargs):
        from ipdb import set_trace
        set_trace()
        return super().post(request, *args, **kwargs)


    def perform_create(self, serializer):
        print("eu cheiguei aqui")
        return serializer.save(guest=self.request.user.id)


class ReservationRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    # mudar para "ser GUEST DONO"
    permission_classes = [IsAuthenticated]
    
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    lookup_url_kwarg = "pk"
