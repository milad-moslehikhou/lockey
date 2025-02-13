from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

app_name = "api"
urlpatterns = [
    path("auth/", include("apps.auth.api.urls", namespace="auth")),
    path("whitelist/", include("apps.whitelist.api.urls", namespace="whitelist")),
    path("permissions/", include("apps.permission.api.urls", namespace="permissions")),
    path("groups/", include("apps.group.api.urls", namespace="groups")),
    path("users/", include("apps.user.api.urls", namespace="users")),
    path("folders/", include("apps.folder.api.urls", namespace="folders")),
    path("credentials/", include("apps.credential.api.urls", namespace="credentials")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path("swagger/", SpectacularSwaggerView.as_view(url_name="api:schema"), name="swagger-ui"),
    path("redoc/", SpectacularRedocView.as_view(url_name="api:schema"), name="redoc"),
]
