from rest_framework import generics
from rest_framework.views import APIView, Response, status
from .models import Employee
from .serializer import EmployeeSerializer
from django.shortcuts import get_object_or_404
from hotel.models import Hotel


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_url_kwarg = "pk"

