from rest_framework import generics
from rest_framework.response import Response
from .serializer import AddressSerializer
from .models import Address
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAddressOwner
from utils.permissions import IsAdmin


class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.exclude(street__endswith="admin")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AddressRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAddressOwner | IsAdmin]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_url_kwarg = "pk"
