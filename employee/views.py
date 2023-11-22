from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView

from utils.auth.authentication import EmailOrUsernameModelBackend
from utils.permissions import IsAdmin, IsAdminOrReadOnly

from .models import Employee
from .permissions import IsEmployeeAndOwner
from .serializer import EmployeeSerializer


class EmployeeListCreateView(ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        hotel_id_parameter = self.request.query_params.get("hotel_id")
        if hotel_id_parameter:
            return Employee.objects.filter(hotel=hotel_id_parameter)

        return super().get_queryset()

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.exclude(username__endswith="admin")

        queryset = queryset.filter(is_staff=True)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AllEmployeeListView(ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdminOrReadOnly]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.exclude(username__endswith="admin")

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class EmployeeRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsEmployeeAndOwner | IsAdmin]

    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    lookup_url_kwarg = "pk"


class EmployeeTokenView(TokenObtainPairView):
    serializer_class = EmailOrUsernameModelBackend

    def post(self, request, *args, **kwargs):
        backend_instance = EmailOrUsernameModelBackend()
        return backend_instance.handle_login_auth(request)
