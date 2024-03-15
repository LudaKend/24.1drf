from rest_framework import generics, status
from users.models import Payment, User
from users.serializer import PaymentSerializer, UserSerializer, MyTokenObtainPairSerializer
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from materials.models import Course
from django.shortcuts import get_object_or_404
from users.services import create_session
from django.conf import settings


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """метод для записи авторизованного пользователя в качестве плательщика """
        payment = serializer.save(user_email=self.request.user)
        payment.save()

    def create(self, request):
        """метод для записи суммы в платежную позицию в таблице Payment, исходя из стоимости курса"""
        #print(request.data)            #для отладки
        temp_course = get_object_or_404(Course, pk=request.data['course'])
        #print(temp_course)             #для отладки
        #print(temp_course.price)       #для отладки
        headers = {'Authorization': settings.STRIPE_TOKEN,
         'Content-Type': 'application/x-www-form-urlencoded',
         'Connection': 'keep-alive'}
        #print(f'id курса из БД{temp_course.id}')     #для отладки
        link = create_session(temp_course.id, headers)
        #print(link)                    #для отладки

        serializer = PaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        payment = serializer.save(payment=temp_course.price*100, link=link)
        payment.save()
        return Response(serializer.data)


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [OrderingFilter, DjangoFilterBackend, SearchFilter]
    search_fields = ['type_payment']

    filterset_fields = ['type_payment', 'course', 'lesson']
    ordering_fields = ['data_pay']
    search_fields = ['payment']

class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """метод для сохранения хешированного пароля в бд (если пароль не хешируется -
        пользователь не считается активным и токен авторизации не создается)"""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)  #здесь хэш генерируем из пароля
        user.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
