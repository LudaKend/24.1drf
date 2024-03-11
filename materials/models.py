from django.db import models
from config import settings

NULLABLE = {'null': True, 'blank': True}

class Course(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание курса', **NULLABLE)
    preview = models.ImageField(upload_to='images/preview_course/', **NULLABLE, verbose_name='Превью курса')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Владелец',
                              **NULLABLE)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='стоимость курса', default=0)

    def __str__(self):
        '''строковое отображение обьекта'''
        return f'{self.name}, {self.price}'

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название урока')
    description = models.TextField(verbose_name='Описание урока', **NULLABLE)
    preview = models.ImageField(upload_to='images/preview_lesson/', **NULLABLE, verbose_name='Превью урока')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING, verbose_name='Владелец',
                              **NULLABLE)

    def __str__(self):
        '''строковое отображение обьекта'''
        return f'{self.name}, {self.course}'

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['id']


class Subscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='Пользователь',
                             related_name='user_from_subscription')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, verbose_name='Курс')
