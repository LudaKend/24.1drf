from rest_framework import generics
from users.models import Payment
from users.serializer import PaymentSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    search_fields = ['type_payment']

    filterset_fields = ['type_payment', 'course', 'lesson']
    ordering_fields = ['data_pay']
    search_fields = ['payment']
