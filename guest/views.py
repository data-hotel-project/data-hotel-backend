from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Guest
from .serializer import GuestSerializer, GuestTokenSerializer


class GuestView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_url_kwarg = "pk"


class GuestTokenView(TokenObtainPairView):
    serializer_class = GuestTokenSerializer
