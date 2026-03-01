from django.db import models
from django.conf import settings


class Category(models.Model):
    """Категории для постов"""
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, verbose_name='URL')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Post(models.Model):
    """Посты (публикации)"""

    POST_TYPES = (
        ('free', 'Бесплатный'),
        ('paid', 'Платный'),
    )

    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    post_type = models.CharField(
        max_length=4,
        choices=POST_TYPES,
        default='free',
        verbose_name='Тип поста'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Категория'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор'
    )
    image = models.ImageField(
        upload_to='posts/',
        blank=True,
        null=True,
        verbose_name='Изображение'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликован')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'

    def __str__(self):
        return self.title

    def can_view(self, user):
        """Проверяет, может ли пользователь просматривать этот пост"""
        if self.post_type == 'free':
            return True
        # Если пост платный, проверяем подписку
        return user.is_authenticated and user.is_subscribed
