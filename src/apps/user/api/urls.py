from rest_framework.routers import DefaultRouter

from .views import UserViewSet

app_name = 'users'
router = DefaultRouter()
router.include_root_view = False
router.register('', UserViewSet, basename='user')
urlpatterns = router.urls
