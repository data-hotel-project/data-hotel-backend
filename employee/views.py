from rest_framework import generics

from .models import Employee
from .serializer import EmployeeSerializer, EmployeeTokenSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .permissions import IsEmployeeAndOwner
from utils.permissions import IsAdmin, IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication


class EmployeeListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class EmployeeRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeAndOwner | IsAdmin]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_url_kwarg = "pk"


class EmployeeTokenView(TokenObtainPairView):
    serializer_class = EmployeeTokenSerializer
