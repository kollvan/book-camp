import uuid
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


def user_image_upload_to(instance: AbstractUser, filename: str):
    date = datetime.now().strftime(format='%Y/%m')
    ext = filename.split('.')[-1]
    return f'image_users/{date}/avatar_{uuid.uuid4().hex}.{ext}'


class User(AbstractUser):
    image = models.ImageField(upload_to=user_image_upload_to, blank=True, null=True, verbose_name='Изображение')
    registration_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    email = models.EmailField(null=False, blank=False, unique=True, verbose_name='E-mail')

    class Meta:
        db_table = 'user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
