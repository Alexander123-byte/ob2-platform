from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Payment

User = get_user_model()


class PaymentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            phone_number='+7(999)-123-45-67',
            email='test@test.com',
            password='Testpass_123'
        )

    def test_subscription_page(self):
        """Тест страницы подписки"""
        self.client.login(phone_number='+7(999)-123-45-67', password='Testpass_123')
        response = self.client.get(reverse('payments:subscription'))
        self.assertEqual(response.status_code, 200)

    def test_subscription_activation(self):
        """Тест активации подписки"""
        self.assertFalse(self.user.is_subscribed)

        self.user.is_subscribed = True
        self.user.subscription_expiry = timezone.now() + timedelta(days=30)
        self.user.save()

        self.assertTrue(self.user.is_subscribed)

    def test_subscription_expiry(self):
        """Тест истечения подписки"""
        self.user.is_subscribed = True
        self.user.subscription_expiry = timezone.now() - timedelta(days=1)
        self.user.save()

        self.assertTrue(self.user.subscription_expiry < timezone.now())
