from rest_framework.routers import DefaultRouter

from .views import (
    CredentialViewSet,
    CredentialSecretViewSet,
    CredentialGrantViewSet,
    CredentialShareViewSet
)

app_name = 'credentials'
router = DefaultRouter()
router.include_root_view = False
router.register('', CredentialViewSet, basename='credential')
router.register('secrets', CredentialSecretViewSet, basename='credential-secret')
router.register('grants', CredentialGrantViewSet, basename='credential-grant')
router.register('shares', CredentialShareViewSet, basename='credential-share')
urlpatterns = router.urls
