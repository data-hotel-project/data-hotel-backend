from . import views
from django.urls import path

urlpatterns = [
    path("", views.RoomView.as_view()),
    path("deleteAll", views.RoomDeleteAllView.as_view()),
    path("<uuid:pk>/", views.RoomDetailView.as_view()),
]
