from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from materials.models import Course, Lesson, Subscription
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionSerializer
from rest_framework.permissions import IsAuthenticated
from users.permission import ModeratorPermissionsClass, UsuallyPermissionsClass, OwnerPermissionsClass
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from materials.paginators import MaterialsPaginator

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator

    def perform_create(self, serializer):
        """метод для записи авторизованного пользователя в качестве владельца """
        course = serializer.save(owner=self.request.user)
        course.save()


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
            owner_queryset = queryset.filter(owner=self.request.user)
            return owner_queryset


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

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        #print(serializer)   #для отладки
        course_id = self.request.data['course']  #получаем id курса из self.request.data
        #print(course_id)  #для отладки
        # получаем список подписок по текущему пользователю:
        #print(self.request.user)
        user_subscription = Subscription.objects.filter(user=request.user, course=course_id)
        #print(user_subscription)    #для отладки
        if user_subscription.exists():
            #print(user_subscription.exists())  #для отладки
        # Если подписка на этот курс есть у пользователя,то удаляем ее
            Subscription.objects.filter(user=request.user, course=course_id).delete()
            #message = 'подписка удалена'
            return Response({"message": "подписка удалена"})
        else:
        # Если подписки у пользователя на этот курс нет,то создаем ее
            if serializer.is_valid():
                serializer.save()
                #message = 'подписка добавлена'
            return Response({"message": "подписка добавлена"})
        #return Response({"message": message})

