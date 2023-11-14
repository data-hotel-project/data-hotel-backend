from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from utils.auth.authentication import EmailOrUsernameModelBackend

from utils.permissions import IsAdmin

from .models import Guest
from .permissions import IsGuestOwner
from .serializer import GuestSerializer


class GuestView(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuestOwner | IsAdmin]

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_url_kwarg = "pk"


class GuestTokenView(TokenObtainPairView, TokenObtainPairSerializer):
    serializer_class = EmailOrUsernameModelBackend

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        username = request.data.get("username")
        password = request.data.get("password")

        if not email and not username or not password:
            return Response(
                {"error": "Both email/username and password are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(request, username=username, email=email, password=password)
        if user.check_password(password):
            refresh = self.get_token(user)

            data = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }

            return Response(data, status=status.HTTP_200_OK)
