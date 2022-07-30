from rest_framework.routers import DefaultRouter

from .views import FolderViewSet

app_name = 'folders'
router = DefaultRouter()
router.include_root_view = False
router.register('', FolderViewSet, basename='folder')
urlpatterns = router.urls
