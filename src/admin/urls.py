from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'PeriodicTask', PeriodicTaskViewSet, r'PeriodicTask')
router.register(r'listTask', ListTasksViewSet, r'listTask')
router.register(r'listBots', ListBotsViewSet, r'listBots')
router.register(r'listCrawlers', ListCrawlersViewSet, r'listCrawlers')


urlpatterns = router.urls
