from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Guest
from .serializer import GuestSerializer, GuestTokenSerializer
from .permissions import IsGuestOwner
from utils.permissions import IsAdmin


class GuestView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuestOwner | IsAdmin]

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_url_kwarg = "pk"


class GuestTokenView(TokenObtainPairView):
    serializer_class = GuestTokenSerializer
