from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
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
