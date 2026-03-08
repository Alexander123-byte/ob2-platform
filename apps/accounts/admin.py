from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User


class UserAdmin(BaseUserAdmin):
    """Настройки админки для пользователей"""

    list_display = (
        'get_full_name', 'phone_number', 'email', 'get_email_verified_status', 'is_subscribed', 'date_joined')
    list_filter = ('email_verified', 'is_subscribed', 'is_staff', 'date_joined')
    search_fields = ('phone_number', 'email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Личная информация', {
            'fields': ('first_name', 'last_name'),
            'classes': ('wide',)
        }),
        ('Email подтверждение', {
            'fields': ('email_verified',),
            'classes': ('wide',),
            'description': 'Отметьте, если пользователь подтвердил email'
        }),
        ('Подписка', {'fields': ('is_subscribed', 'subscription_expiry')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone_number', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    ordering = ('-date_joined',)
    list_per_page = 25

    def get_full_name(self, obj):
        """Отображает полное имя"""
        if obj.first_name and obj.last_name:
            return f"{obj.last_name} {obj.first_name}"
        return obj.phone_number

    get_full_name.short_description = 'ФИО'
    get_full_name.admin_order_field = 'last_name'

    def get_email_verified_status(self, obj):
        """Отображает статус подтверждения email с иконкой"""
        if obj.email_verified:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Подтверждён</span>'
            )
        else:
            return format_html(
                '<span style="color: orange;">○ Ожидает</span>'
            )

    get_email_verified_status.short_description = 'Email статус'
    get_email_verified_status.admin_order_field = 'email_verified'


admin.site.register(User, UserAdmin)
