from rest_framework import routers

from .views import *

router = routers.DefaultRouter()

router.register(r'periodicTask', PeriodicTaskViewSet, r'periodicTask')
router.register(r'listTask', ListTasksViewSet, r'listTask')
router.register(r'listBots', ListBotsViewSet, r'listBots')
router.register(r'listCrawlers', ListCrawlersViewSet, r'listCrawlers')
router.register(r'schedule', ScheduleViewSet, r'schedule')
router.register(r'deleteTask', DeleteTaskViewSet, r'deleteTask')

urlpatterns = router.urls
