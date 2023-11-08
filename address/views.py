from rest_framework import generics
from rest_framework.views import APIView, Response, status
from .serializer import AddressSerializer
from .models import Address

class AddressListCreateView(generics.ListCreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

class AddressRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer