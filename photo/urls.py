from django.urls import path
from . import views

urlpatterns = [
    path("", views.PhotoListCreateView.as_view()),
    path("<uuid:pk>/", views.PhotoRetrieveUpdateDeleteView.as_view()),
]