from rest_framework import generics, views
from employee.models import Employee
from .serializer import EmployeeSerializer


class EmployeeView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
