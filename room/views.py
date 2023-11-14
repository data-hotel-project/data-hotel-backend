from rest_framework import generics

from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.permissions import IsAdminOrReadOnly
from .models import Room
from .serializer import RoomSerializer
from .permissions import IsStaff
from utils.permissions import IsAdmin


class RoomView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff | IsAdmin]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "pk"
