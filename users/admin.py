from admin_confirm import AdminConfirmMixin, confirm_action
from django.contrib import admin, messages

from inventory.models import Inventory
from users.models import User


# Register your models here.

class InventoryUser(admin.TabularInline):
    verbose_name = 'Запись в инвентарь'
    verbose_name_plural = 'Записи в инвентаре'
    model = Inventory
    fields = ['product', 'status', 'rank', 'date_added']
    search_fields = ['product', 'rank']
    readonly_fields = ['rank', 'date_added']

    extra = 1
@admin.register(User)
class UserAdmin(AdminConfirmMixin, admin.ModelAdmin):
    confirm_change = True
    save_on_top = True
    list_display = ['username', 'email', 'registration_date' ,'is_staff']
    fields = ['image', 'registration_date', 'username', 'first_name',
              'last_name', 'email', 'is_staff', 'is_superuser', 'last_login', 'groups', 'user_permissions']
    readonly_fields = ['registration_date', 'last_login', 'email']
    search_fields = ['username', 'email', 'registration_date']
    inlines = [InventoryUser,]
    actions = ['clear_inventory', 'add_in_staff', 'remove_in_staff']

    @admin.action(description='Очистить инвентарь')
    @confirm_action
    def clear_inventory(self, request, queryset):
        count = 0
        for user in queryset:
            count += Inventory.objects.filter(user=user).delete()[0]
        self.message_user(request, f'Инвентари очищены. Удалено записей из инвентарей {count}.')

    @admin.action(description='Сделать персоналом')
    @confirm_action
    def add_in_staff(self, request, queryset):
        count = len(queryset)
        for user in queryset:
            user.is_staff = True
            user.save()
        self.message_user(
            request,
    f'Пользователям предоставленны права персонала. Количество пользователей {count}.',
            level=messages.WARNING
        )

    @admin.action(description='Удалить из персонала')
    @confirm_action
    def remove_in_staff(self, request, queryset):
        count = len(queryset)
        for user in queryset:
            user.is_staff = False
            user.save()
        self.message_user(
            request,
            f'Пользователи убраны из персонала. Количество пользователей {count}.',
            level=messages.WARNING
        )