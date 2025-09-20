from django.core.validators import MaxValueValidator
from django.db import models

from goods.models import Product
from users.models import User


# Create your models here.
class Inventory(models.Model):
    class Status(models.IntegerChoices):
        STARTED = 3, 'Начато'
        POSTPONED = 2, 'Отложено'
        ADDED = 1, 'Добавлено'
        COMPLETED = 0, 'Завершено'


    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.IntegerField(choices=Status, default=Status.ADDED, db_index=True, verbose_name='Состояние')
    rank = models.IntegerField(default=0,
                               validators=[MaxValueValidator(5)],
                               verbose_name='Оценка')


    product = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, db_index=True, verbose_name='Книга')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')


    class Meta:
        db_table = 'inventory'
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентари'
        unique_together = ('product', 'user',)

