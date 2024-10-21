from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Lockey API",
        default_version='v1',
        description="API documentation for Lockey secret management app",
        contact=openapi.Contact(email="milad.moslehikhou@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

app_name = 'api'
urlpatterns = [
    path(r'auth/', include('apps.auth.api.urls', namespace='auth')),
    path(r'whitelist/', include('apps.whitelist.api.urls', namespace='whitelist')),
    path(r'permissions/', include('apps.permission.api.urls', namespace='permissions')),
    path(r'groups/', include('apps.group.api.urls', namespace='groups')),
    path(r'users/', include('apps.user.api.urls', namespace='users')),
    path(r'folders/', include('apps.folder.api.urls', namespace='folders')),
    path(r'credentials/', include('apps.credential.api.urls', namespace='credentials')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
