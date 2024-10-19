from django.urls import path
from knox import views as knox_views

from apps.auth.api.views import LoginView

app_name = 'auth'
urlpatterns = [
    path(r'login/', LoginView.as_view(), name='knox_login'),
    path(r'logout/', knox_views.LogoutView.as_view(), name='knox_logout'),
    path(
        r'logoutall/',
        knox_views.LogoutAllView.as_view(),
        name='knox_logoutall'),
]
