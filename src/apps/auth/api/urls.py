from django.urls import path

from apps.auth.api.views import LoginView, LogoutAllView, LogoutView

app_name = "auth"
urlpatterns = [
    path("login/", LoginView.as_view(), name="knox_login"),
    path("logout/", LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", LogoutAllView.as_view(), name="knox_logoutall"),
]
