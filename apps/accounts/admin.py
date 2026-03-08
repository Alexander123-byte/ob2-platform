from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils import timezone
from .models import User


class UserAdmin(BaseUserAdmin):
    """Настройки админки для пользователей"""

    list_display = (
        'phone_number', 'email', 'email_verified_status', 'verification_info', 'is_subscribed', 'date_joined')
    list_filter = ('email_verified', 'is_subscribed', 'is_staff', 'date_joined')
    search_fields = ('phone_number', 'email')

    fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'password')}),
        ('Персональная информация', {'fields': ('first_name', 'last_name')}),
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
            'fields': ('phone_number', 'email', 'password1', 'password2'),
        }),
    )

    ordering = ('-date_joined',)
    list_per_page = 25

    def email_verified_status(self, obj):
        """Отображает статус подтверждения email с иконкой"""
        if obj.email_verified:
            return format_html(
                '<span style="color: green; font-weight: bold;">✓ Подтверждён</span>'
            )
        else:
            return format_html(
                '<span style="color: orange;">○ Ожидает</span>'
            )

    email_verified_status.short_description = 'Email'
    email_verified_status.admin_order_field = 'email_verified'

    def verification_info(self, obj):
        """Дополнительная информация о верификации"""
        if obj.email_verified:
            return format_html(
                '<span style="color: #28a745;">✔ Верифицирован</span>'
            )
        else:
            time_since_joined = timezone.now() - obj.date_joined
            if time_since_joined.days > 0:
                return format_html(
                    '<span style="color: #dc3545;">⚠ Требует внимания</span>'
                )
            return format_html(
                '<span style="color: #6c757d;">Ожидание подтверждения</span>'
            )

    verification_info.short_description = 'Статус'


admin.site.register(User, UserAdmin)
