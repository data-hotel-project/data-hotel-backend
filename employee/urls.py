from django.urls import path
from employee import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('', views.EmployeeListCreateView.as_view()),
    path('<int:pk>/', views.EmployeeRetrieveUpdateDeleteView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
]