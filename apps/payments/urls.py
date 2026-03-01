from django.urls import path
from .views import (
    SubscriptionView, create_payment,
    payment_success, payment_cancel, payment_webhook
)

app_name = 'payments'

urlpatterns = [
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('create-payment/', create_payment, name='create_payment'),
    path('success/', payment_success, name='success'),
    path('cancel/', payment_cancel, name='cancel'),
    path('webhook/', payment_webhook, name='webhook'),
]
