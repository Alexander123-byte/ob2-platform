from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class UserManager(BaseUserManager):
    """Менеджер пользователей для работы без username"""

    def create_user(self, phone_number, email, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя
        """
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        if not email:
            raise ValueError('Email обязателен')

        email = self.normalize_email(email)
        user = self.model(phone_number=phone_number, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, password=None, **extra_fields):
        """
        Создает и сохраняет суперпользователя
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Суперпользователь должен иметь is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Суперпользователь должен иметь is_superuser=True')

        return self.create_user(phone_number, email, password, **extra_fields)


class User(AbstractUser):
    """Custom user model with phone number authentication"""

    username = None

    phone_number = models.CharField(
        max_length=18,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\+7\(\d{3}\)-\d{3}-\d{2}-\d{2}$',
            message="Номер телефона должен быть в формате: +7(999)-999-99-99"
        )]
    )

    email = models.EmailField(unique=True)

    is_subscribed = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(null=True, blank=True)
    email_verified = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def get_absolute_url(self):
        """Возвращает URL профиля пользователя"""
        return reverse('content:post_list')

    def __str__(self):
        return f"{self.phone_number} - {self.email}"
