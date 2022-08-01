from rest_framework.routers import DefaultRouter

from apps.credential.api.views import (
    CredentialViewSet
)

app_name = 'credentials'
router = DefaultRouter()
router.include_root_view = False
router.register('', CredentialViewSet, basename='credential')
urlpatterns = router.urls
