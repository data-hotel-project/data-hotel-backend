from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.permissions import IsAdmin, IsAdminOrReadOnly

from .models import Room
from .permissions import IsStaff
from .serializer import RoomSerializer


class RoomView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    def get_queryset(self):
        hotel_id_parameter = self.request.query_params.get("hotel_id")
        if hotel_id_parameter:
            return Room.objects.filter(hotel=hotel_id_parameter)

        return super().get_queryset()


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsStaff | IsAdmin]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "pk"


class RoomDeleteAllView(generics.DestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def destroy(self, request, *args, **kwargs):
        Room.objects.all().delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
