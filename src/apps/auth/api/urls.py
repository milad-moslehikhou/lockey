from django.urls import path

from apps.auth.api.views import LoginView, LogoutView, LogoutAllView


app_name = 'auth'
urlpatterns = [
    path('login/', LoginView.as_view(), name='api-login'),
    path('logout/', LogoutView.as_view(), name='api-logout'),
    path('logout_all/', LogoutAllView.as_view(), name='api-logout-all'),
]
