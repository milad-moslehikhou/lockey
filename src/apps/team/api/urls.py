from rest_framework.routers import DefaultRouter

from apps.team.api.views import TeamViewSet

app_name = 'teams'
router = DefaultRouter()
router.include_root_view = False
router.register('', TeamViewSet, basename='team')
urlpatterns = router.urls
