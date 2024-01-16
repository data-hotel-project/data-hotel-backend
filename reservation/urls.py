from django.urls import path
from reservation import views

urlpatterns = [
    path("", views.ReservationListCreateView.as_view()),
    path("deleteAll", views.ReservationDeleteAllView.as_view()),
    path("<uuid:pk>/", views.ReservationRetrieveUpdateDeleteView.as_view()),
]
