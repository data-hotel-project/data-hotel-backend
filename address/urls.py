from django.urls import path
from address import views

urlpatterns = [
    path("", views.AddressListCreateView.as_view()),
    path("<uuid:pk>/", views.AddressRetrieveUpdateDeleteView.as_view()),
]