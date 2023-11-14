from rest_framework import generics

from .models import Employee
from .serializer import EmployeeSerializer, EmployeeTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_url_kwarg = "pk"


class EmployeeTokenView(TokenObtainPairView):
    serializer_class = EmployeeTokenSerializer
