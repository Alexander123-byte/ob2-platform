from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Настройки админки для категорий"""
    list_display = ('name', 'slug', 'post_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def post_count(self, obj):
        """Считает количество постов в категории"""
        return obj.posts.count()

    post_count.short_description = 'Количество постов'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Настройки админки для постов"""
    list_display = ('title', 'author', 'category', 'post_type', 'created_at', 'is_published')
    list_filter = ('post_type', 'category', 'is_published', 'created_at')
    search_fields = ('title', 'content', 'author__phone_number')
    raw_id_fields = ('author',)
    date_hierarchy = 'created_at'
    list_editable = ('is_published',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'content', 'author')
        }),
        ('Настройки', {
            'fields': ('post_type', 'category', 'image', 'is_published')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
