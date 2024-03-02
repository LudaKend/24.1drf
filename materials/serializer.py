from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from materials.models import Course, Lesson, Subscription
from materials.validators import WrongLinkValidator
from users.serializer import UserSerializer
import json


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [WrongLinkValidator(field='name'), WrongLinkValidator(field='description')]


class CourseSerializer(serializers.ModelSerializer):

    lessons = LessonSerializer(many=True, read_only=True, source='lesson_set')
    quantity_lesson = SerializerMethodField()

    subscriptions = SubscriptionSerializer(many=True, read_only=True, source='subscription_set')
    user = UserSerializer(read_only=True)
    #subscriptions = SerializerMethodField()


    def get_quantity_lesson(self, course):
        list_lesson = Lesson.objects.filter(course=course)
        print(list_lesson)  #для отладки
        return len(list_lesson)

    # def get_object(self, queryset):
    #     print(f'queryset {queryset}')
    #     return self.request.user

    def get_subscriptions(self, obj):
        print(obj)
        #user = self.request.user
        #user = self.get_object()
        list_subscription = Subscription.objects.filter(course=obj)
        print(f'list:{list_subscription}')
        print(obj.subscription_set.all())
        print(type(list_subscription))

        # json_string = json.dumps(list(list_subscription))
        # print(json_string)
        # print(type(json_string))
        #print(obj.subscription_set.filter(user=self.user))
        for pos in list_subscription:
            print(pos)
            #print(pos.user_from_subscription)
        #    return pos.user
        #    return pos
        #return list_subscription


    class Meta:
        model = Course
        fields = ['name', 'description', 'quantity_lesson', 'lessons', 'subscriptions', 'user', ]
        validators = [WrongLinkValidator(field='name'), WrongLinkValidator(field='description')]

