from rest_framework import generics
from rest_framework.response import Response

from .models import Hotel
from .serializer import HotelSerializer


class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.exclude(name__endswith="admin")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class HotelRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    lookup_url_kwarg = "pk"
