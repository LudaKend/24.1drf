from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from materials.models import Course, Lesson



class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):

    quantity_lesson = SerializerMethodField()

    def get_quantity_lesson(self, course):
        list_lesson = Lesson.objects.filter(course=course)
        return len(list_lesson)

    class Meta:
        model = Course
        fields = '__all__'

