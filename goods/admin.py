from django.contrib import admin

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

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = [
        'name', 'slug', 'image', 'author', 'quantity_page', 'year_of_publication', 'datetime_added', 'category', 'tags',
        'description',
    ]
    prepopulated_fields = {'slug':('name',)}
    readonly_fields = ['datetime_added',]