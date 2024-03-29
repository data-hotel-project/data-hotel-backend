from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("", views.EmployeeListCreateView.as_view()),
    path("all/", views.AllEmployeeListView.as_view()),
    path("<uuid:pk>/", views.EmployeeRetrieveUpdateDeleteView.as_view()),
    path("login/", views.EmployeeTokenView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),
]
