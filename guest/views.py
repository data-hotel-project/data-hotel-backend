from rest_framework import generics

from .models import Employee
from .serializer import EmployeeSerializer


class GuestView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class GuestDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_url_kwarg = "pk"
