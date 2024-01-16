from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path("", views.GuestView.as_view()),
    path("<uuid:pk>/", views.GuestDetailView.as_view()),
    path("login/", views.GuestTokenView.as_view(), name="token_obtain_guest"),
    path("refresh/", TokenRefreshView.as_view()),
]
