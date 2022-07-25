from django.urls import path
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView


app_name = 'dashboard'
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='change-password'),

    path('home/', TemplateView.as_view(template_name='home.html')),
    path('setting/', TemplateView.as_view(template_name='setting.html')),
]
