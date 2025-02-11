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

class Tag(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Slug')

    class Meta:
        db_table = 'tag'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Author(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Имя')
    slug = models.SlugField(max_length=100, unique=True, verbose_name='Slug')

    class Meta:
        db_table = 'author'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(max_length=150, verbose_name='Slug', db_index=True)
    image = models.ImageField(upload_to='image_books', blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey(to=Author, on_delete=models.SET_DEFAULT, default='Неизвестный автор')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    quantity_page = models.PositiveSmallIntegerField(verbose_name='Количество страниц')
    year_of_publication = models.CharField(max_length=4, blank=True, null=True, verbose_name='Год публикации')
    datetime_added = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    category = models.ForeignKey(to=Category, on_delete=models.CASCADE, verbose_name='Категория')
    tags = models.ManyToManyField(to=Tag, related_name='product_tag', blank=True, verbose_name='Теги')

    class Meta:
        db_table = 'product'
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

        ordering = ['name',]

    def get_tags(self):
        return Product.objects.get(pk=self.pk).tags.all()

    def __str__(self):
        return f'{self.name} | Автор: {self.author.name}'