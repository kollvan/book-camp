from django.contrib import admin

from goods.models import Category, Tag


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug':('name', )}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}