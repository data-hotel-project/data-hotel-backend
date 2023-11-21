from django.urls import path
from . import views

urlpatterns = [
    path("", views.GetLoggedUser.as_view()),
]