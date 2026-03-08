from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    phone_number = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7(999)-999-99-99',
            'id': 'phone-input'
        })
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'user@example.com'
        })
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иван'
        })
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов'
        })
    )
    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label='Подтверждение пароля',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('phone_number', 'email', 'first_name', 'last_name')

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        digits = ''.join(filter(str.isdigit, phone))

        if len(digits) != 11:
            raise forms.ValidationError('Номер телефона должен содержать 11 цифр')

        if digits[0] not in ['7', '8']:
            raise forms.ValidationError('Номер должен начинаться с 7 или 8')

        if digits[0] == '8':
            digits = '7' + digits[1:]

        formatted = f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

        if User.objects.filter(phone_number=formatted).exists():
            raise forms.ValidationError('Пользователь с таким номером уже существует')

        return formatted

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not first_name:
            raise forms.ValidationError('Имя обязательно')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not last_name:
            raise forms.ValidationError('Фамилия обязательна')
        return last_name


class PhoneNumberLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7(999)-999-99-99',
            'id': 'login-phone-input'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')

        digits = ''.join(filter(str.isdigit, username))

        if len(digits) != 11:
            raise forms.ValidationError('Номер телефона должен содержать 11 цифр')

        if digits[0] not in ['7', '8']:
            raise forms.ValidationError('Номер должен начинаться с 7 или 8')

        if digits[0] == '8':
            digits = '7' + digits[1:]

        formatted = f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

        return formatted


class UserSettingsForm(forms.ModelForm):
    """Форма редактирования профиля пользователя"""

    phone_number = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+7(999)-999-99-99',
            'id': 'settings-phone-input'
        }),
        required=True
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'user@example.com'
        }),
        required=True
    )
    first_name = forms.CharField(
        label='Имя',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иван'
        }),
        required=True
    )
    last_name = forms.CharField(
        label='Фамилия',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Иванов'
        }),
        required=True
    )

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')

        if self.user and self.user.phone_number == phone:
            return phone

        digits = ''.join(filter(str.isdigit, phone))

        if len(digits) != 11:
            raise forms.ValidationError('Номер телефона должен содержать 11 цифр')

        if digits[0] not in ['7', '8']:
            raise forms.ValidationError('Номер должен начинаться с 7 или 8')

        if digits[0] == '8':
            digits = '7' + digits[1:]

        formatted = f"+7({digits[1:4]})-{digits[4:7]}-{digits[7:9]}-{digits[9:11]}"

        if User.objects.filter(phone_number=formatted).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Пользователь с таким номером уже существует')

        return formatted

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if self.user and self.user.email == email:
            return email

        if User.objects.filter(email=email).exclude(pk=self.user.pk).exists():
            raise forms.ValidationError('Пользователь с таким email уже существует')

        return email
