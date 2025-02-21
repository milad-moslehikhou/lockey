from django.urls import path

from apps.auth.api.views import (
    EnableOtpView,
    LoginView,
    LogoutView,
    RefreshTokenView,
    VerifyOtpView,
)

app_name = "auth"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh_token"),
    path("enable-2fa/", EnableOtpView.as_view(), name="enable_2fa"),
    path("verify-2fa/", VerifyOtpView.as_view(), name="verify_2fa"),
]
