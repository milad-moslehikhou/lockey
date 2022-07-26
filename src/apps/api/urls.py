from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('users', include('apps.user.api.urls', namespace='users')),
    path('teams', include('apps.team.api.urls', namespace='teams')),
    path('credentials', include('apps.credential.api.urls', namespace='credentials')),
]
