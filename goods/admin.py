from django.contrib import admin
from django.utils.safestring import mark_safe

from goods.models import Category, Tag, Author, Product


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name', )}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class ProductsAuthor(admin.TabularInline):
    verbose_name = 'Книга'
    verbose_name_plural = 'Книги'
    model = Product
    fields = ['name', 'slug', 'year_of_publication', 'datetime_added']
    search_fields = ['name', 'year_of_publication']
    readonly_fields = ['datetime_added',]
    extra = 0

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}
    inlines = [ProductsAuthor,]




@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
         'name', 'slug', 'show_image','image', 'author',
        'quantity_page', 'year_of_publication', 'datetime_added', 'category', 'tags',
        'description',
    ]
    prepopulated_fields = {'slug':('name',)}
    readonly_fields = ['datetime_added', 'show_image',]

    # def save_model(self, request, obj, form, change):
    #     print(form.cleaned_data['image'])
    #     super().save_model(request, obj, form, change)

    @admin.display(description='Image', ordering='name')
    def show_image(self, product):
        if product.image:
            return mark_safe(f'<img src="{product.image.url}" width="100">')
        return 'None'