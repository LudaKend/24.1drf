from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from materials.models import Course, Lesson
from materials.validators import WrongLinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [WrongLinkValidator(field='name'), WrongLinkValidator(field='description')]


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    quantity_lesson = SerializerMethodField()


    def get_quantity_lesson(self, course):
        list_lesson = Lesson.objects.filter(course=course)
        print(list_lesson)
        return len(list_lesson)

    # def get_list_lesson(self, course):
    #     list_lesson = Lesson.objects.filter(course=course)
    #     return list_lesson

    class Meta:
        model = Course
        fields = ['name', 'description', 'quantity_lesson', 'lessons', ]
        validators = [WrongLinkValidator(field='name'), WrongLinkValidator(field='description')]

