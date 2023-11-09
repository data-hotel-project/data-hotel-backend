from . import views
from django.urls import path

urlpatterns = [
    path("", views.GuestView.as_view()),
    path("<uuid:pk>/", views.GuestDetailView.as_view()),
]
