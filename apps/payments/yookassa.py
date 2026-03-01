import uuid
from yookassa import Configuration, Payment
from django.conf import settings


Configuration.account_id = settings.YOOKASSA_SHOP_ID
Configuration.secret_key = settings.YOOKASSA_SECRET_KEY


class YookassaClient:
    """Класс для работы с ЮКасса"""
    def create_payment(self, amount, user, description, return_url):
        """Создание платежа"""

        idempotency_key = str(uuid.uuid4())

        payment = Payment.create({
            "amount": {
                "value": f"{amount}.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": return_url
            },
            "capture": True,
            "description": description,
            "metadata": {
                "user_id": user.id,
                "user_phone": user.phone_number
            }
        }, idempotency_key)

        return payment

    def get_payment_info(self, payment_id):
        """Получение информации о платеже"""
        return Payment.find_one(payment_id)
