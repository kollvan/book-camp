from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        db_table = 'category'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name