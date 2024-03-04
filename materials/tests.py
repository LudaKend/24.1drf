from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User
from materials.models import Lesson, Course, Subscription
from django.urls import reverse
from django.contrib.auth.models import Group

class CourseTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='autotest@mail.ru', password='init_init')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='для теста', description='для автотеста', owner=self.user)

    def test_get_list(self):
        response = self.client.get('/materials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.json(), [{'count': 1, 'next': None, 'previous': None, 'results': [
        #     {'name': 'для теста', 'description': 'для автотеста', 'quantity_lesson': 0,
        #                                     'lessons': [], 'subscriptions': []}]}])
        # self.assertEqual(response.json(), [{'name': 'для теста', 'description': 'для автотеста', 'quantity_lesson': 0,
        #      'lessons': [], 'subscriptions': []}])
        self.assertTrue(Course.objects.filter(id=self.course.id).exists())


class LessonTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='autotest@mail.ru', password='init_init')
        self.client.force_authenticate(user=self.user)
        #force_authenticate(request, user=user, token=user.auth_token) из документации

        self.course = Course.objects.create(name='для теста', description='для автотеста', owner=self.user)
        self.lesson = Lesson.objects.create(name='для теста', description='для автотеста', course=self.course,
                                            owner=self.user)
        self.data = {'name': 'test', 'description': 'для автотеста', 'course': self.course.id, 'owner': self.user.id}


    def test_get_list(self):
        response = self.client.get('/list_view/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.json(), [{'id': self.lesson.id, 'name': 'для теста', 'description': 'для автотеста',
        #                                     'preview': None, 'course': self.course.id, 'owner': self.user.id}])
        self.assertTrue(Lesson.objects.filter(id=self.lesson.id).exists())

    def test_post(self):
        response = self.client.post('/create/', self.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(response.json(), [{'id': 2, 'name': 'test', 'description': 'для автотеста',
        #                                     'preview': None, 'course': self.course.id, 'owner': self.user.id}])
        self.assertTrue(Lesson.objects.filter(name='test').exists())
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_post_moderator(self):
        self.user_group = Group.objects.create(name="moderator")   #создаю группу
        self.user.groups.add(self.user_group)                 #юзеру нужно присвоить группу модератор
        response = self.client.post('/create/', self.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


    def test_update(self):
        self.url = reverse('materials:lesson_update', kwargs={'pk': self.lesson.id})
        response = self.client.put(self.url, self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Lesson.objects.filter(name='test').exists())


    def test_delete(self):
        self.url = reverse('materials:lesson_delete', kwargs={'pk': self.lesson.id})
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(id=self.lesson.id).exists())


class SubscriptionTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create(email='autotest@mail.ru', password='init_init')
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(name='для теста', description='для автотеста', owner=self.user)
        self.data = {'course': self.course.id}

    def test_add(self):
        response = self.client.post('/subscription/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка добавлена"})
        self.assertTrue(Subscription.objects.filter(user=self.user.id, course=self.course.id).exists())


    def test_del(self):
        self.subscription = Subscription.objects.create(user=self.user, course=self.course)
        response = self.client.post('/subscription/', self.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {"message": "подписка удалена"})
        self.assertFalse(Subscription.objects.filter(user=self.user.id, course=self.course.id).exists())
