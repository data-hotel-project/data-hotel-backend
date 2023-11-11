from rest_framework import generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import Employee
from .serializer import EmployeeSerializer, EmployeeTokenSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_url_kwarg = "pk"


class EmployeeTokenView(TokenObtainPairView):
    serializer_class = EmployeeTokenSerializer
