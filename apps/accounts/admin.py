from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    """Настройки админки для пользователей"""

    # Поля, отображаемые в списке пользователей
    list_display = ('phone_number', 'email', 'is_subscribed', 'is_staff',
                    'date_joined')
    list_filter = ('is_subscribed', 'is_staff', 'is_superuser', 'groups')
    search_fields = ('phone_number', 'email')

    # Поля для просмотра и редактирования пользователя
    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
        ('Подписка', {'fields': ('is_subscribed', 'subscription_expiry')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                      'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    # Поля для создания нового пользователя
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'password1', 'password2'),
        }),
    )

    ordering = ('phone_number',)


# Регистрируем модель User в админке
admin.site.register(User, UserAdmin)
