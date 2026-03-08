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
        fields = ('phone_number', 'email')

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
