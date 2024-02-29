from django.shortcuts import get_object_or_404
from rest_framework import viewsets, generics
from materials.models import Course, Lesson
from materials.serializer import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from users.permission import ModeratorPermissionsClass, UsuallyPermissionsClass, OwnerPermissionsClass
from django.http import Http404

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def perform_create(self, serializer):
        """метод для записи авторизованного пользователя в качестве владельца """
        course = serializer.save(owner=self.request.user)
        course.save()


    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, ModeratorPermissionsClass | OwnerPermissionsClass]
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
        if self.request.user.is_staff:
            print(self.request.user.is_staff)
            return queryset
        else:
            owner_queryset = queryset.filter(owner=self.request.user)
            return owner_queryset


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]

    def perform_create(self, serializer):
        """метод для записи авторизованного пользователя в качестве владельца """
        print(self.request.user)
        lesson = serializer.save(owner=self.request.user)
        lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ModeratorPermissionsClass | OwnerPermissionsClass]

    def get_queryset(self):
        queryset = super().get_queryset()
        #print(queryset)
        #print(self.request.user.is_staff)
        if self.request.user.is_staff:
            print(self.request.user.is_staff)
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
