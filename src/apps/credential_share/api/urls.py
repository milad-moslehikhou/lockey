from rest_framework.routers import DefaultRouter

from apps.credential_share.api.views import (
    CredentialShareViewSet
)

app_name = 'share'
router = DefaultRouter()
router.include_root_view = False
router.register('', CredentialShareViewSet, basename='share')
urlpatterns = router.urls
