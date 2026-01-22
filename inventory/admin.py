from django.contrib import admin

from inventory.models import Inventory


# Register your models here.
@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    fields = ['date_added', 'status', 'rank', 'user', 'product', 'review']
    readonly_fields = ['date_added', 'status', 'rank', 'user', 'product', 'review']
    list_display = ['id','date_added', 'status', 'rank', 'user', 'product']
    list_display_links = ['id', 'date_added',]