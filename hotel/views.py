from rest_framework import generics
from rest_framework.views import APIView, Response, status
from .models import Hotel
from .serializer import HotelSerializer
from address.models import Address

class HotelListCreateView(generics.ListCreateAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer

    def post(self, request):


        serializer = HotelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address_data = serializer.validated_data.pop("address")
        print(address)
        address = Address.objects.create(**address_data)

        hotel = Hotel.objects.create(address=address, **serializer.validated_data)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class HotelRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
