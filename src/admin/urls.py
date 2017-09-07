from rest_framework import routers
from .views import CrontabsViewSet


router = routers.DefaultRouter()
router.register(r'crontabs', CrontabsViewSet, r'crontabs')


urlpatterns = router.urls
