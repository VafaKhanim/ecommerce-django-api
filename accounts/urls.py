from django.urls import path
from .views import (
    RegisterView,
    SellerRegisterView,  # New view
    LoginView,
    LogoutView,
    PasswordResetRequestView,
    SetNewPasswordView
)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('register/seller/', SellerRegisterView.as_view(), name='seller-register'),  # New path
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset'),
    path('password-reset-confirm/', SetNewPasswordView.as_view(), name='password-reset-confirm'),
]