from rest_framework.routers import DefaultRouter

from .views import (
    CredentialViewSet,
    CredentialCategoryViewSet,
    CredentialSecretViewSet,
    CredentialGrantViewSet,
    CredentialShareViewSet
)

app_name = 'credentials'
router = DefaultRouter()
router.include_root_view = False
router.register('', CredentialViewSet, basename='credential')
router.register('', CredentialCategoryViewSet, basename='credential-category')
router.register('', CredentialSecretViewSet, basename='credential-secret')
router.register('', CredentialGrantViewSet, basename='credential-grant')
router.register('', CredentialShareViewSet, basename='credential-share')
urlpatterns = router.urls
