from rest_framework import generics
from .serializer import CustomUserSerializer
from .models import CustomUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from utils.permissions import IsAuthenticated
from rest_framework.response import Response

class GetLoggedUser(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CustomUserSerializer

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user)
        return Response(serializer.data)

