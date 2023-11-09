from rest_framework import generics

from .models import Room
from .serializer import RoomSerializer


class RoomView(generics.ListCreateAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = RoomSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)

    #     # from ipdb import set_trace

    #     # set_trace()

    #     serializer.save()


class RoomDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    lookup_url_kwarg = "pk"
