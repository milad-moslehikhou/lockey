from django.urls import path

from apps.auth.api.views import EnableOtpView, LoginView, LogoutAllView, LogoutView, VerifyOtpView

app_name = "auth"
urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", LogoutAllView.as_view(), name="knox_logoutall"),
    path("enable2fa/", EnableOtpView.as_view(), name="enable_2fa"),
    path("verify2fa/", VerifyOtpView.as_view(), name="verify_2fa"),
]
