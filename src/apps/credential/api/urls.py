from django.urls import path

from .views import CredentialsView, CredentialView

app_name = 'credentials'
urlpatterns = [
    path('', CredentialsView.as_view()),
    path('<int:pk>/', CredentialView.as_view()),
]
