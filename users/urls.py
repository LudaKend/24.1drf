from users.apps import UsersConfig
from users.views import PaymentListAPIView
from django.urls import path


app_name = UsersConfig.name

urlpatterns = [

    path('payment_list_view/', PaymentListAPIView.as_view(), name='payment_list'),
    ]
