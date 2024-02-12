from django.db import models
from django.contrib.auth.models import AbstractUser

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
