from rest_framework import generics

from .models import Guest
from .serializer import GuestSerializer


class GuestView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_url_kwarg = "pk"
