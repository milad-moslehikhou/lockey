from django.urls import path, include

app_name = 'api'
urlpatterns = [
    path(r'auth/', include('apps.auth.api.urls', namespace='auth')),
    path(
        r'whitelist/',
        include(
            'apps.whitelist.api.urls',
            namespace='whitelist')),
    path(
        r'permissions/',
        include(
            'apps.permission.api.urls',
            namespace='permissions')),
    path(r'groups/', include('apps.group.api.urls', namespace='groups')),
    path(r'users/', include('apps.user.api.urls', namespace='users')),
    path(r'folders/', include('apps.folder.api.urls', namespace='folders')),
    path(
        r'credentials/',
        include(
            'apps.credential.api.urls',
            namespace='credentials')),
]
