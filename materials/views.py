from django.shortcuts import render
from rest_framework import viewsets, generics
from materials.models import Course, Lesson
from materials.serializer import CourseSerializer, LessonSerializer
from rest_framework.permissions import IsAuthenticated
from users.permission import ModeratorPermissionsClass, UsuallyPermissionsClass

class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]
        elif self.action == 'list':
            self.permission_classes = [IsAuthenticated, ModeratorPermissionsClass]
        elif self.action == 'retrieve':
            self.permission_classes = [IsAuthenticated, ModeratorPermissionsClass]
        elif self.action == 'update':
            self.permission_classes = [IsAuthenticated, ModeratorPermissionsClass]
        elif self.action == 'destroy':
            self.permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]

        print([permission() for permission in self.permission_classes])
        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]

class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ModeratorPermissionsClass]

class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ModeratorPermissionsClass]

class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ModeratorPermissionsClass]

class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, ~ModeratorPermissionsClass]
