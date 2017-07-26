from rest_framework import routers
from .views import *


router = routers.DefaultRouter()
router.register(r'calllinkage', CallLinkageViewSet, r'calllinkage')
router.register(r'organizationlinkage', OrganizationLinkageViewSet, r'organizationlinkage')
router.register(r'projectlinkage', ProjectLinkageViewSet, r'projectlinkage')
router.register(r'personlinkage', PersonLinkageViewSet, r'personlinkage')

urlpatterns = router.urls
