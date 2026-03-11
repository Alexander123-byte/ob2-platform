from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (UserRegistrationView, UserLoginView, verify_email,
                    ProfileView, SettingsView, ResendVerificationEmailView)

app_name = 'accounts'

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('verify/<uidb64>/<token>/', verify_email, name='verify_email'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('settings/', SettingsView.as_view(), name='settings'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend_verification'),
]
