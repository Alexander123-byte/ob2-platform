from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import logging

logger = logging.getLogger(__name__)


def send_verification_email(user, request):
    """Отправляет письмо с подтверждением email"""

    try:
        # Создаём токен для подтверждения
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Ссылка для подтверждения
        verification_url = request.build_absolute_uri(
            reverse('accounts:verify_email', kwargs={
                'uidb64': uid,
                'token': token
            })
        )

        subject = 'Подтверждение email на OB2 Platform'

        message = f'''
        Здравствуйте, {user.phone_number}!

        Для подтверждения вашего email перейдите по ссылке:
        {verification_url}

        Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.

        С уважением,
        Команда OB2 Platform
        '''

        # Отправляем письмо
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )

        return True

    except Exception as e:
        print(f"Ошибка при отправке письма: {e}")
        logger.error(f"Failed to send verification email to {user.email}: {e}")
        return False
