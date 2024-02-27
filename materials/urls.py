from materials.apps import MaterialsConfig
from rest_framework.routers import DefaultRouter
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,\
    LessonUpdateAPIView, LessonDestroyAPIView, LessonAllListAPIView
from django.urls import path


app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'materials', CourseViewSet, basename='course')

urlpatterns = [
    path('create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('list_view/', LessonListAPIView.as_view(), name='lesson_list'),
    path('all_list_view/', LessonAllListAPIView.as_view(), name='lesson_all_list'),
    path('view/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_view'),
    path('update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
              ] + router.urls
