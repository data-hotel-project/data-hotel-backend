from . import views
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path("", views.EmployeeListCreateView.as_view()),
    path("<uuid:pk>/", views.EmployeeRetrieveUpdateDeleteView.as_view()),
    path("login/", TokenObtainPairView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
