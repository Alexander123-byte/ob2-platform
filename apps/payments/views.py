import json
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.utils import timezone
from datetime import timedelta
from .models import Subscription, Payment


class SubscriptionView(LoginRequiredMixin, TemplateView):
    """Страница оформления подписки"""
    template_name = 'payments/subscription.html'


@login_required
def create_payment(request):
    """Создание платежа через ЮKassa"""
    import uuid
    import requests
    from django.conf import settings
    from django.shortcuts import redirect

    try:
        shop_id = settings.YOOKASSA_SHOP_ID
        secret_key = settings.YOOKASSA_SECRET_KEY

        idempotence_key = str(uuid.uuid4())

        url = "https://api.yookassa.ru/v3/payments"

        payment_data = {
            "amount": {
                "value": "1000.00",
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": request.build_absolute_uri(reverse('payments:success'))
            },
            "capture": True,
            "description": f"Подписка для {request.user.phone_number}",
            "metadata": {
                "user_id": request.user.id,
                "user_phone": request.user.phone_number
            }
        }

        response = requests.post(
            url,
            json=payment_data,
            auth=(shop_id, secret_key),
            headers={
                "Idempotence-Key": idempotence_key,
                "Content-Type": "application/json"
            }
        )

        result = response.json()

        if response.status_code == 200 or response.status_code == 201:
            request.session['pending_payment_id'] = result['id']
            request.session['pending_payment_amount'] = 1000

            Payment.objects.create(
                user=request.user,
                yookassa_payment_intent_id=result['id'],
                amount=1000,
                status='pending'
            )

            return JsonResponse({
                'success': True,
                'payment_url': result['confirmation']['confirmation_url'],
                'payment_id': result['id']
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result.get('description', 'Ошибка при создании платежа')
            })

    except Exception as e:
        print(f"Ошибка: {e}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        })


@login_required
def payment_success(request):
    """Страница успешной оплаты"""
    from yookassa import Payment as YooPayment
    from django.conf import settings

    from yookassa import Configuration
    Configuration.account_id = settings.YOOKASSA_SHOP_ID
    Configuration.secret_key = settings.YOOKASSA_SECRET_KEY

    activated = False
    payment_info = None

    payment_id = request.session.get('pending_payment_id')

    if payment_id:
        try:
            payment = YooPayment.find_one(payment_id)
            payment_info = payment

            if payment.status == 'succeeded':
                Payment.objects.filter(
                    yookassa_payment_intent_id=payment_id,
                    user=request.user
                ).update(status='succeeded')

                user = request.user
                user.is_subscribed = True
                user.subscription_expiry = timezone.now() + timedelta(days=30)
                user.save()

                Subscription.objects.update_or_create(
                    user=user,
                    defaults={
                        'yookassa_subscription_id': payment_id,
                        'expires_at': timezone.now() + timedelta(days=30),
                        'is_active': True
                    }
                )

                activated = True

                del request.session['pending_payment_id']

            elif payment.status == 'pending':
                return render(request, 'payments/success.html', {
                    'activated': False,
                    'pending': True,
                    'payment_id': payment_id
                })

        except Exception as e:
            print(f"Ошибка при проверке платежа: {e}")

    return render(request, 'payments/success.html', {
        'activated': activated,
        'payment': payment_info
    })


def payment_cancel(request):
    """Страница отмены оплаты"""
    return render(request, 'payments/cancel.html')


@csrf_exempt
@require_POST
def payment_webhook(request):
    """Webhook для уведомлений от ЮKassa"""
    try:
        data = json.loads(request.body)

        if data.get('event') == 'payment.succeeded':
            payment = data.get('object', {})
            payment_id = payment.get('id')

            payment_obj = Payment.objects.filter(
                yookassa_payment_intent_id=payment_id
            ).first()

            if payment_obj:
                payment_obj.status = 'succeeded'
                payment_obj.save()

                user = payment_obj.user
                user.is_subscribed = True
                user.subscription_expiry = timezone.now() + timedelta(days=30)
                user.save()

                Subscription.objects.update_or_create(
                    user=user,
                    defaults={
                        'yookassa_subscription_id': payment_id,
                        'expires_at': timezone.now() + timedelta(days=30),
                        'is_active': True
                    }
                )

        return HttpResponse(status=200)

    except Exception as e:
        print(f"Webhook error: {e}")
        return HttpResponse(status=400)
