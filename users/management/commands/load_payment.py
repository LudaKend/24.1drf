from django.core.management import BaseCommand
from pathlib import Path
import json
from materials.models import Course, Lesson
from users.models import User, Payment
from django.shortcuts import get_object_or_404

class Command(BaseCommand):
    def handle(self, *args, **options):
        #Payment.objects.all().delete()
        #Payment.truncate_table_restart_id()
        list_payment = self.load_from_json()
        print(list_payment)

        for item in list_payment:
            #сначала нужно вытянуть по foreign key значение email_user из таблицы User
            fk = item['fields']['user_email']
            print(fk)
            try:
                user_email = User.objects.get(email=fk) #get_object_or_404(User, email=fk)
                print(user_email)
            except:
                #если плательщик не опознан, то платеж запишем на служебного пользователя
                user_email = User.objects.get(email='admin@mail.ru')
                print(user_email)

            # сначала нужно вытянуть по foreign key id курса из таблицы Course
            fk = item['fields']['course']
            print(fk)
            try:
                course = Course.objects.get(pk=fk)
            except:
                #если курс в платежке не указан или указан неверно, то записываем вспомогательное значение курса
                #в БД создала запись:
                # insert into materials_course values (1, 'не указан', 'в платеже курс не указан или указан неверно')
                course = Course.objects.get(pk=1)
                print(course)

            # сначала нужно вытянуть по foreign key значение lesson из таблицы Lesson
            fk = item['fields']['lesson']
            print(fk)
            try:
                lesson = Lesson.objects.get(pk=fk)
            except:
                # если урок в платежке не указан или указан неверно, то записываем вспомогательное значение урока
                # в БД создала запись:
                # insert into materials_course values (6, 'не указан', 'все уроки, указанного в платеже курса', null, 1)
                lesson = Lesson.objects.get(pk=6)
                print(lesson)

            # из фикстуры json беру fields
            payment_create = item['fields']
            print(payment_create)   # для отладки

            # в поля 'user_email', 'course', 'lesson', которые являются foreign key, django позволяет записать только,
            # если подставить значение, которое вытащишь из соответствующей таблицы User, Course, 'Lesson'

            payment_create['user_email'] = user_email
            payment_create['course'] = course
            payment_create['lesson'] = lesson

            print(payment_create)   # для отладки

            # создаем запись в таблице:
            Payment.objects.create(**payment_create)

    def load_from_json(self):
        '''Загружает в список платежи из файла json'''
        json_path = Path(__file__).parent.joinpath('fixtura_payment.json')
        print(json_path)  # для отладки
        with open(json_path, encoding='utf-8') as file:
            payment_json = json.loads(file.read())
        return payment_json
