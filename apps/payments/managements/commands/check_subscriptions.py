from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.payments.models import Subscription
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Проверяет и деактивирует просроченные подписки'

    def handle(self, *args, **options):
        expired_users = User.objects.filter(
            is_subscribed=True,
            subscription__expiry__lt=timezone.now()
        )

        count = expired_users.count()

        for user in expired_users:
            user.is_subscribed = False
            user.save()

            Subscription.objects.filter(user=user).update(is_active=False)

        self.stdout.write(
            self.style.SUCCESS(f'Деактивировано {count} просроченных подписок')
        )
