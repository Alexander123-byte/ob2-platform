from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView
from django.shortcuts import redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from .forms import UserRegistrationForm, PhoneNumberLoginForm
from .models import User
from .utils import send_verification_email
import logging

logger = logging.getLogger(__name__)


class UserRegistrationView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Отправляем письмо с подтверждением
        try:
            email_sent = send_verification_email(self.object, self.request)
            if email_sent:
                messages.success(
                    self.request,
                    'Регистрация успешна! Проверьте вашу почту для подтверждения email.'
                )
            else:
                messages.warning(
                    self.request,
                    'Регистрация успешна, но не удалось отправить письмо с подтверждением.'
                )
        except Exception as e:
            print(f"Ошибка в form_valid: {e}")
            messages.warning(
                self.request,
                'Регистрация успешна, но не удалось отправить письмо с подтверждением.'
            )

        return response


class UserLoginView(LoginView):
    form_class = PhoneNumberLoginForm
    template_name = 'accounts/login.html'


def verify_email(request, uidb64, token):
    """Подтверждение email"""
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.email_verified = True
        user.save()
        messages.success(request, 'Email успешно подтверждён! Теперь вы можете войти.')
        return redirect('accounts:login')
    else:
        messages.error(request, 'Ссылка для подтверждения недействительна или устарела.')
        return redirect('content:post_list')
