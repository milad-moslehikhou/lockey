from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path('auth/', include('apps.auth.api.urls', namespace='auth')),
    path('whitelist/', include('apps.whitelist.api.urls', namespace='whitelist')),
    path('groups/', include('apps.group.api.urls', namespace='groups')),
    path('users/', include('apps.user.api.urls', namespace='users')),
    path('teams/', include('apps.team.api.urls', namespace='teams')),
    path('folders/', include('apps.folder.api.urls', namespace='folders')),
    path('credentials/', include('apps.credential.api.urls', namespace='credentials')),
]
