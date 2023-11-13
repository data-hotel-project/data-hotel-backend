from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.permissions import IsAdminOrReadOnly
from .models import Room
from .serializer import RoomSerializer


class RoomView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAdminOrReadOnly]


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "pk"
