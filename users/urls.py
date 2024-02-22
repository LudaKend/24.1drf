from users.apps import UsersConfig
from users.views import PaymentListAPIView, UserCreateAPIView, MyTokenObtainPairView, UserRetrieveAPIView
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

app_name = UsersConfig.name

urlpatterns = [

    path('payment_list_view/', PaymentListAPIView.as_view(), name='payment_list'),
    path('token/', MyTokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('register/', UserCreateAPIView.as_view(), name='register_users'),
    path('view/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_view'),
    ]
