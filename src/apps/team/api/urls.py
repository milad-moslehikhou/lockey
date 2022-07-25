from django.urls import path

from .views import TeamsView, TeamView

app_name = 'teams'
urlpatterns = [
    path('', TeamsView.as_view()),
    path('<int:pk>/', TeamView.as_view())
]
