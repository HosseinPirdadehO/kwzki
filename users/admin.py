from django.contrib import admin
from .models import CustomUser

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number',
                    'position', 'is_admin', 'is_active')
    list_filter = ('is_admin', 'is_active', 'position')
    search_fields = ('first_name', 'last_name', 'phone_number', 'username')
