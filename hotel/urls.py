from django.urls import path
from hotel import views

urlpatterns = [
    path("", views.HotelListCreateView.as_view()),
    path("<uuid:pk>/", views.HotelRetrieveUpdateDeleteView.as_view()),
]