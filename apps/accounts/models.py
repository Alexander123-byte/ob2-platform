from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone


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

    # Убираем поле username
    username = None

    # Добавляем номер телефона как основное поле
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message="Номер телефона должен быть в формате: '+79991234567'"
        )]
    )

    # Email теперь обязательный и уникальный
    email = models.EmailField(unique=True)

    # Поля для подписки
    is_subscribed = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(null=True, blank=True)

    # Привязываем менеджер
    objects = UserManager()

    # Говорим Django, что поле для входа - номер телефона
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return f"{self.phone_number} - {self.email}"
