from rest_framework.routers import DefaultRouter

from .views import WhitelistViewSet

app_name = 'whitelist'
router = DefaultRouter()
router.include_root_view = False
router.register('', WhitelistViewSet, basename='whitelist')
urlpatterns = router.urls
