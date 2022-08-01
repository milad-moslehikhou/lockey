from rest_framework.routers import DefaultRouter

from apps.group.api.views import GroupViewSet

app_name = 'groups'
router = DefaultRouter()
router.include_root_view = False
router.register('', GroupViewSet, basename='group')
urlpatterns = router.urls
