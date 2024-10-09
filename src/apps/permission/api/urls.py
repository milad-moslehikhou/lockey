from rest_framework.routers import DefaultRouter

from apps.permission.api.views import PermissionViewSet

app_name = 'permission'
router = DefaultRouter()
router.include_root_view = False
router.register('', PermissionViewSet, basename='permission')
urlpatterns = router.urls
