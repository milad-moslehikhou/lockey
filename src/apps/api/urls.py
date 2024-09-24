from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path(r'auth/', include('apps.auth.api.urls', namespace='auth')),
    path(r'whitelist/', include('apps.whitelist.api.urls', namespace='whitelist')),
    path(r'groups/', include('apps.group.api.urls', namespace='groups')),
    path(r'users/', include('apps.user.api.urls', namespace='users')),
    path(r'teams/', include('apps.team.api.urls', namespace='teams')),
    path(r'folders/', include('apps.folder.api.urls', namespace='folders')),
    path(r'credentials/', include('apps.credential.api.urls', namespace='credentials')),
    path(r'share/', include('apps.credential_share.api.urls', namespace='share')),
]
