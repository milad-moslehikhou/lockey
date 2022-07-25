from django.urls import path

from .views import UsersView, UserView

app_name = 'users'
urlpatterns = [
    path('', UsersView.as_view()),
    path('<int:pk>/', UserView.as_view())
]
