from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from .forms import UserRegistrationForm, PhoneNumberLoginForm
from .models import User


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    # Изменяем 'login' на 'accounts:login'
    success_url = reverse_lazy('accounts:login')  # Вот здесь исправление!


class UserLoginView(LoginView):
    form_class = PhoneNumberLoginForm
    template_name = 'accounts/login.html'
