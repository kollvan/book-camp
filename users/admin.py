from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    fields = ['image', 'registration_date', 'username','first_name', 'last_name', 'email']
    readonly_fields = ['registration_date',]