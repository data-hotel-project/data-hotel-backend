from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.auth.authentication import EmailOrUsernameModelBackend
from utils.permissions import IsAdmin

from .models import Guest
from .permissions import IsGuestAndOwner
from .serializer import GuestSerializer


class GuestView(ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer


class GuestDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsGuestAndOwner | IsAdmin]

    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    lookup_url_kwarg = "pk"


class GuestTokenView(TokenObtainPairView):
    serializer_class = EmailOrUsernameModelBackend

    def post(self, request, *args, **kwargs):
        backend_instance = EmailOrUsernameModelBackend()
        return backend_instance.handle_login_auth(request)
