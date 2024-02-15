from django.db import models
from django.contrib.auth.models import AbstractUser
from materials.models import Course, Lesson

NULLABLE = {'null': True, 'blank': True}

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='почта')
    phone = models.CharField(max_length=30, verbose_name='Телефон', **NULLABLE)
    city = models.CharField(max_length=30, verbose_name='Город', **NULLABLE)
    avatar = models.ImageField(upload_to='images/avatar/', **NULLABLE, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        '''строковое отображение обьекта'''
        return f'{self.email}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Payment(models.Model):
    user_email = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='email студента', **NULLABLE)
    data_pay = models.DateField(verbose_name='дата оплаты')
    course = models.ForeignKey(Course, on_delete=models.DO_NOTHING, verbose_name='оплаченный курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.DO_NOTHING, verbose_name='оплаченный урок', **NULLABLE)
    payment = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='сумма платежа')
    type_payment = models.CharField(max_length=100, verbose_name='способ платежа')

    def __str__(self):
        '''строковое отображение обьекта'''
        return f'{self.user_email}, {self.course}, {self.lesson}'

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
