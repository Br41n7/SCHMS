"""
URL patterns for accounts app.
"""
from django.urls import path
from .views import (
    RegisterView,
    CustomLoginView,
    CustomLogoutView,
    ProfileUpdateView,
    CustomPasswordResetView,
    CustomPasswordResetConfirmView
)

app_name = 'accounts'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('password-reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         CustomPasswordResetConfirmView.as_view(), 
         name='password_reset_confirm'),
]