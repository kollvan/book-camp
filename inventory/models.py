from django.db import models

from goods.models import Product
from users.models import User


# Create your models here.
class Inventory(models.Model):
    class Status(models.IntegerChoices):
        COMPLETED = 3, 'Завершённый'
        STARTED = 2, 'Начатый'
        POSTPONED = 1, 'Отложенный'
        ADDED = 0, 'Добавленный'

    date_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    status = models.IntegerField(choices=Status, default=Status.ADDED, verbose_name='Состояние')
    rank = models.DecimalField(max_digits=2, decimal_places=2, default=0.00, verbose_name='Оценка')


    product = models.ForeignKey(to=Product, on_delete=models.DO_NOTHING, verbose_name='Книга')
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, verbose_name='Пользователь')

    class Meta:
        db_table = 'inventory'
        verbose_name = 'Инвентарь'
        verbose_name_plural = 'Инвентари'
        unique_together = ('product', 'user',)

