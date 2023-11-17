from rest_framework import generics
from .serializer import PhotoSerializer
from .models import Photo
from rest_framework_simplejwt.authentication import JWTAuthentication

from room.permissions import IsStaff
from utils.permissions import IsAdmin


class PhotoListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff | IsAdmin]

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

    def get_queryset(self):
        hotel_id_parameter = self.request.query_params.get("hotel_id")
        room_id_parameter = self.request.query_params.get("room_id")
        if hotel_id_parameter:
            return Photo.objects.filter(hotel=hotel_id_parameter)
        if room_id_parameter:
            return Photo.objects.filter(room=room_id_parameter)


class PhotoRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff | IsAdmin]

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    lookup_url_kwarg = "pk"
