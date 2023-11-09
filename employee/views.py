from rest_framework import generics
from rest_framework.views import APIView, Response, status
from .models import Employee
from .serializer import EmployeeSerializer
from django.shortcuts import get_object_or_404
from hotel.models import Hotel
from address.models import Address

class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


    def post(self, request, pk):

        # hotel = get_object_or_404(Hotel, pk=pk)

        serializer = EmployeeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        address = serializer.validated_data.pop("address")
        Address.objects.create(**address)

        hotel_id = serializer.validated_data.pop("hotel")
        hotel = get_object_or_404(Hotel, hotel_id)

        serializer.save(hotel=hotel)

        return Response(data=serializer.data, status=status.HTTP_201_CREATED)

class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

