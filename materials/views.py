from rest_framework import viewsets, generics
from materials.models import Course, Lesson, Subscription, Stripe
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer, StripeSerializer
from rest_framework.permissions import IsAuthenticated
from users.permission import ModeratorPermissionsClass, OwnerPermissionsClass
from rest_framework.views import APIView
from rest_framework.response import Response
from materials.paginators import MaterialsPaginator
from django.shortcuts import get_object_or_404
from users.services import create_product, create_price
from django.conf import settings

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        """метод для записи авторизованного пользователя в качестве владельца """
        course = serializer.save(owner=self.request.user)
        course.save()
        #print(f'id созданного курса {course.id}')     #для отладки
        return course.id

    def create(self, request):
        """метод для создания записи в таблице Stripe"""
        #print(request.data)            #для отладки
        headers = {'Authorization': settings.STRIPE_TOKEN,
                   'Content-Type': 'application/x-www-form-urlencoded',
                   'Connection': 'keep-alive'}
        stripe_product = create_product(request.data['name'], headers)
        #print(stripe_product)          #для отладки
        #print(stripe_product['id'])    #для отладки

        stripe_price = create_price(stripe_product['id'], headers)
        #print(stripe_price)            #для отладки
        #serializer = StripeSerializer(data=request.data, stripe_product=stripe_product['id'], stripe_price=stripe_price['id'])
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        id_course = self.perform_create(serializer)
        Stripe.objects.create(course_id=id_course, stripe_product=stripe_product['id'], stripe_price=stripe_price['id'])
        return Response(serializer.data)


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated] #, ModeratorPermissionsClass | UsuallyPermissionsClass]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, ModeratorPermissionsClass | OwnerPermissionsClass]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, ModeratorPermissionsClass | OwnerPermissionsClass]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, OwnerPermissionsClass]
        #print([permission() for permission in self.permission_classes])  #для отладки
        return [permission() for permission in self.permission_classes]

    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.request.user.is_staff:
        #     print(self.request.user.is_staff)
        if self.request.user.groups.filter(name='moderator').exists():
            return queryset
        else:
            #print(self.request.user)   # для отладки
            # owner_queryset = queryset.filter(owner=self.request.user)
            # return owner_queryset
            if not self.request.user.is_anonymous:
                owner_queryset = queryset.filter(owner=self.request.user)
                return owner_queryset
            return None


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]

    def perform_create(self, serializer):
        """метод для записи авторизованного пользователя в качестве владельца """
        #print(self.request.user)   #для отладки
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated] #, ModeratorPermissionsClass | UsuallyPermissionsClass]
    pagination_class = MaterialsPaginator

    def get_queryset(self):
        queryset = super().get_queryset()
        # if self.request.user.is_staff:
        #     print(self.request.user.is_staff)
        if self.request.user.groups.filter(name='moderator').exists():
            return queryset
        else:
            owner_queryset = queryset.filter(owner=self.request.user)
            return owner_queryset


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ModeratorPermissionsClass | OwnerPermissionsClass]

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ModeratorPermissionsClass | OwnerPermissionsClass]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, OwnerPermissionsClass]


class SubscriptionAPIView(APIView):
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        #print(request.data)  #для отладки
        serializer = SubscriptionSerializer(data=request.data)
        #print(serializer)   #для отладки
        course_id = self.request.data['course']  #получаем id курса из self.request.data
        #print(course_id)  #для отладки
        # получаем список подписок по текущему пользователю:
        user_subscription = Subscription.objects.filter(user=self.request.user, course=course_id)
        #print(user_subscription)    #для отладки
        if user_subscription.exists():
            #print(user_subscription.exists())  #для отладки
        # Если подписка на этот курс есть у пользователя,то удаляем ее
            Subscription.objects.filter(user=self.request.user, course=course_id).delete()
            #message = 'подписка удалена'
            return Response({"message": "подписка удалена"})
        else:
        # Если подписки у пользователя на этот курс нет,то создаем ее
            if serializer.is_valid():
                #temp_course = Course.objects.filter(id=course_id)
                temp_course = get_object_or_404(Course, id=course_id)
                #print(temp_course)
                Subscription.objects.create(user=self.request.user, course=temp_course)
                #message = 'подписка добавлена'
            return Response({"message": "подписка добавлена"})
        #return Response({"message": message})

