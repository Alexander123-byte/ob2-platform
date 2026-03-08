from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator
from django.urls import reverse


class UserManager(BaseUserManager):
    """Менеджер пользователей для работы без username"""

    def create_user(self, phone_number, email, first_name, last_name, password=None, **extra_fields):
        """
        Создает и сохраняет обычного пользователя
        """
        if not phone_number:
            raise ValueError('Номер телефона обязателен')
        if not email:
            raise ValueError('Email обязателен')
        if not first_name:
            raise ValueError('Имя обязательно')
        if not last_name:
            raise ValueError('Фамилия обязательна')

        email = self.normalize_email(email)
        user = self.model(
            phone_number=phone_number,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, first_name, last_name, password=None, **extra_fields):
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

        return self.create_user(phone_number, email, first_name, last_name, password, **extra_fields)


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

    first_name = models.CharField(max_length=30, verbose_name='Имя')
    last_name = models.CharField(max_length=30, verbose_name='Фамилия')

    email_verified = models.BooleanField(default=False)

    is_subscribed = models.BooleanField(default=False)
    subscription_expiry = models.DateTimeField(null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

    def get_full_name(self):
        """Возвращает полное имя"""
        return f"{self.last_name} {self.first_name}".strip()

    def get_short_name(self):
        """Возвращает короткое имя"""
        return self.first_name

    def get_absolute_url(self):
        """Возвращает URL профиля пользователя"""
        return reverse('accounts:profile')

    def save(self, *args, **kwargs):
        if self.phone_number and not self.phone_number.startswith('+7('):
            digits = ''.join(filter(str.isdigit, self.phone_number))
            if len(digits) == 11 and digits.startswith('7'):
                self.phone_number = f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
            elif len(digits) == 11 and digits.startswith('8'):
                digits = '7' + digits[1:]
                self.phone_number = f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"
        super().save(*args, **kwargs)
