from rest_framework import generics

from .models import Hotel
from .serializer import HotelSerializer


class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer


class HotelRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    lookup_url_kwarg = "pk"
