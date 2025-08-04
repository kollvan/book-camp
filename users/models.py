from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    image = models.ImageField(upload_to='image_users', blank=True, null=True, verbose_name='Изображение')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name='E-mail')


    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username