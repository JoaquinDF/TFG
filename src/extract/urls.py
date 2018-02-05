from rest_framework import routers
from .views import BotViewSet, CrawlerViewSet, DataViewSet

router = routers.DefaultRouter()
router.register(r'bot', BotViewSet, r'bot')
router.register(r'crawler', CrawlerViewSet, r'crawler')
router.register(r'data', DataViewSet, r'dada')

urlpatterns = router.urls
